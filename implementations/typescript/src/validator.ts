import fs from "node:fs";
import path from "node:path";
import YAML from "yaml";

export const statuses = ["proposed", "ready", "in-progress", "blocked", "validation", "done", "superseded", "deferred"] as const;
const statusSet = new Set<string>(statuses);
const terminal = new Set(["done", "superseded", "deferred"]);
const authorities = new Set(["repository", "tracker", "manual"]);
const slugPattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

type RecordValue = Record<string, unknown>;
type Parsed = { metadata: RecordValue; body: string };

const secretPatterns: Array<[string, RegExp]> = [
  ["private key", /-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----/],
  ["GitHub token", /\bgh[pousr]_[A-Za-z0-9_]{20,}\b/],
  ["AWS access key", /\bAKIA[0-9A-Z]{16}\b/],
  ["assigned secret", /\b(?:api[_-]?key|access[_-]?token|secret|password)\s*[:=]\s*["']?[A-Za-z0-9_./+=-]{12,}/i],
];
const machinePathPatterns: Array<[string, RegExp]> = [
  ["file URI", /\bfile:\/\//i],
  ["Windows absolute path", /(?:^|[^A-Za-z0-9])(?:[A-Za-z]:[\\/]|\\\\)[^\s<>'"]+/],
  ["POSIX machine path", /(?:^|[^A-Za-z0-9])\/(?:home|Users|tmp|var\/tmp|etc|opt|srv|root|mnt|Volumes)\/[^\s<>'"]+/],
  ["home-relative path", /(?:^|[^A-Za-z0-9])~[\\/][^\s<>'"]+/],
];

function markdownFiles(root: string): string[] {
  if (!fs.existsSync(root)) return [];
  return fs.readdirSync(root, { withFileTypes: true }).flatMap((entry) => {
    const candidate = path.join(root, entry.name);
    return entry.isDirectory() ? markdownFiles(candidate) : entry.isFile() && entry.name.endsWith(".md") ? [candidate] : [];
  }).sort();
}

function parseDocument(file: string): Parsed {
  const source = fs.readFileSync(file, "utf8");
  if (!source.startsWith("---\n") && !source.startsWith("---\r\n")) throw new Error(`Missing YAML frontmatter in ${file}`);
  const match = source.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
  if (!match) throw new Error(`Unclosed YAML frontmatter in ${file}`);
  let metadata: unknown;
  try { metadata = YAML.parse(match[1]); } catch (error) { throw new Error(`Invalid YAML frontmatter in ${file}: ${String(error)}`); }
  if (!metadata || typeof metadata !== "object" || Array.isArray(metadata)) throw new Error(`Frontmatter must be a mapping in ${file}`);
  return { metadata: metadata as RecordValue, body: source.slice(match[0].length).replace(/^\r?\n/, "") };
}

export function egressFindings(text: string, root: string): string[] {
  const findings: string[] = [];
  const roots = [path.resolve(root), path.resolve(root).replaceAll("\\", "/")].map((value) => value.toLowerCase());
  text.split(/\r?\n/).forEach((line, index) => {
    for (const [name, pattern] of secretPatterns) if (pattern.test(line)) findings.push(`line ${index + 1}: detected ${name}`);
    for (const [name, pattern] of machinePathPatterns) if (pattern.test(line)) findings.push(`line ${index + 1}: detected ${name}`);
    if (roots.some((value) => value && line.toLowerCase().includes(value))) findings.push(`line ${index + 1}: detected repository-local absolute path`);
  });
  return [...new Set(findings)];
}

function repositoryWebBase(remote: string, requestedProvider?: string): { provider: "github" | "gitlab"; base: string } {
  let host: string; let repositoryPath: string;
  const scp = !remote.includes("://") ? remote.trim().match(/^(?:[^@/]+@)?([^:]+):(.+)$/) : null;
  if (scp) { [, host, repositoryPath] = scp; }
  else {
    let parsed: URL; try { parsed = new URL(remote); } catch { throw new Error("Unsupported repository remote"); }
    if (!["http:", "https:", "ssh:", "git:"].includes(parsed.protocol) || !parsed.hostname) throw new Error("Unsupported repository remote");
    host = parsed.host; repositoryPath = parsed.pathname.replace(/^\//, "");
  }
  repositoryPath = repositoryPath.replace(/\.git$/, "").replace(/^\/+|\/+$/g, "");
  let provider = requestedProvider;
  const hostname = host.split(":", 1)[0].toLowerCase();
  if (!provider && (hostname === "github.com" || hostname.endsWith(".github.com"))) provider = "github";
  if (!provider && hostname.includes("gitlab")) provider = "gitlab";
  if (provider !== "github" && provider !== "gitlab") throw new Error("Repository provider is not identifiable");
  const encoded = repositoryPath.split("/").map((part) => encodeURIComponent(decodeURIComponent(part))).join("/");
  return { provider, base: `https://${host}/${encoded}` };
}

export function prepareExternalArtifact(
  rootValue: string,
  sourceValue: string,
  remote: string,
  ref: string,
  requestedProvider?: string,
  allowRemoteImages = false,
): string {
  const root = path.resolve(rootValue); const source = path.resolve(root, sourceValue);
  const relativeSource = path.relative(root, source);
  if (relativeSource.startsWith("..") || path.isAbsolute(relativeSource)) throw new Error("Source document must remain inside the repository root");
  const { body } = parseDocument(source);
  const findings = egressFindings(body, root);
  if (findings.length) throw new Error(findings.join("\n"));
  const { provider, base } = repositoryWebBase(remote, requestedProvider);
  const encodedRef = encodeURIComponent(ref);
  const rendered = body.replace(/(!)?(\[[^\]\n]*\])\(([^)\s]+)([^)]*)\)/g, (original, image: string | undefined, label: string, rawTarget: string, suffix: string) => {
    const target = rawTarget.replace(/^<|>$/g, "");
    if (target.startsWith("#")) return original;
    if (/^[A-Za-z][A-Za-z0-9+.-]*:/.test(target)) {
      if (!target.startsWith("https://")) throw new Error("External artifact contains a non-HTTPS or machine-local link");
      if (image && !allowRemoteImages) throw new Error("External artifact contains a remote image without an explicit allow policy");
      return original;
    }
    if (target.startsWith("//") || /^[A-Za-z]:[\\/]/.test(target)) throw new Error("External artifact contains a machine-local absolute link");
    const [withoutFragment, fragment = ""] = target.split("#", 2);
    if (withoutFragment.includes("?")) throw new Error("Repository-local links with query strings are not portable");
    const localPath = decodeURIComponent(withoutFragment).replaceAll("\\", "/");
    const candidate = path.resolve(localPath.startsWith("/") ? root : path.dirname(source), localPath.replace(/^\//, ""));
    const relative = path.relative(root, candidate);
    if (relative.startsWith("..") || path.isAbsolute(relative)) throw new Error("External artifact contains a repository link outside the declared root");
    if (!fs.existsSync(candidate)) throw new Error("External artifact contains an unresolved repository-local link");
    const view = fs.statSync(candidate).isDirectory() ? "tree" : "blob";
    const encodedPath = relative.split(path.sep).map((part) => encodeURIComponent(part)).join("/");
    const encodedFragment = fragment ? `#${encodeURIComponent(decodeURIComponent(fragment))}` : "";
    const providerPath = provider === "gitlab" ? `-/${view}` : view;
    return `${image ?? ""}${label}(${base}/${providerPath}/${encodedRef}/${encodedPath}${encodedFragment}${suffix})`;
  });
  const provenance = `<!-- OKF Tasks export: source=${relativeSource.replaceAll("\\", "/")}; revision=${ref} -->\n\n`;
  const output = provenance + rendered.replace(/\s+$/, "") + "\n";
  const finalFindings = egressFindings(output, root);
  if (finalFindings.length) throw new Error(finalFindings.join("\n"));
  return output;
}

function heading(body: string, name: string): boolean {
  return new RegExp(`^##\\s+${name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\s*$`, "m").test(body);
}

function rfc3339(value: unknown): boolean {
  return typeof value === "string" && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/.test(value) && !Number.isNaN(Date.parse(value));
}

function nonNegativeInteger(value: unknown): boolean { return Number.isInteger(value) && Number(value) >= 0; }
function mapping(value: unknown): value is RecordValue { return !!value && typeof value === "object" && !Array.isArray(value); }

function validateEstimate(file: string, task: RecordValue, errors: string[]): void {
  if (task.estimate !== undefined) {
    if (!mapping(task.estimate)) errors.push(`${file}: estimate must be a mapping`);
    else {
      const estimate = task.estimate;
      if (!nonNegativeInteger(estimate.effort_minutes)) errors.push(`${file}: estimate.effort_minutes must be a non-negative integer`);
      if (!["agent", "manual", "historical"].includes(String(estimate.method))) errors.push(`${file}: estimate.method is invalid`);
      if (!["low", "medium", "high"].includes(String(estimate.confidence))) errors.push(`${file}: estimate.confidence is invalid`);
      if (!estimate.basis || !estimate.actor || !rfc3339(estimate.timestamp)) errors.push(`${file}: estimate missing required fields`);
    }
  }
  if (task.sprint_points !== undefined) {
    if (!mapping(task.sprint_points)) errors.push(`${file}: sprint_points must be a mapping`);
    else {
      const points = task.sprint_points;
      if (typeof points.value !== "number" || points.value < 0) errors.push(`${file}: sprint_points.value must be a non-negative number`);
      if (typeof points.scale !== "string" || !points.scale.trim()) errors.push(`${file}: sprint_points.scale is required`);
      if (!rfc3339(points.timestamp)) errors.push(`${file}: sprint_points.timestamp must be RFC 3339`);
    }
  }
}

function validateSync(file: string, task: RecordValue, errors: string[]): void {
  if (task.external !== undefined) {
    if (!Array.isArray(task.external)) errors.push(`${file}: external must be a list`);
    else task.external.forEach((item, index) => {
      if (!mapping(item) || !item.system || item.id === undefined || item.id === "" || !item.url) errors.push(`${file}: external[${index}] requires system, id, and url`);
    });
  }
  if (task.sync !== undefined) {
    if (!mapping(task.sync)) errors.push(`${file}: sync must be a mapping`);
    else {
      if (!authorities.has(String(task.sync.authority))) errors.push(`${file}: sync.authority must be repository, tracker, or manual`);
      if (task.sync.field_authority !== undefined) {
        if (!mapping(task.sync.field_authority)) errors.push(`${file}: sync.field_authority must be a mapping`);
        else Object.entries(task.sync.field_authority).forEach(([field, authority]) => {
          if (!authorities.has(String(authority))) errors.push(`${file}: sync.field_authority.${field} must be repository, tracker, or manual`);
        });
      }
    }
  }
}

function validateTime(taskFile: string, task: RecordValue, errors: string[]): void {
  const timeDir = path.join(path.dirname(taskFile), "time");
  const files = fs.existsSync(timeDir) ? fs.readdirSync(timeDir).filter((name) => name.endsWith(".md")).map((name) => path.join(timeDir, name)).sort() : [];
  const entries: RecordValue[] = [];
  const running = new Map<string, string>();
  for (const file of files) {
    let parsed: Parsed; try { parsed = parseDocument(file); } catch { continue; }
    const entry = parsed.metadata; entries.push(entry);
    const required = ["type", "task", "entry", "status", "actor", "started", "method", "timestamp"];
    const missing = required.filter((key) => entry[key] === undefined || entry[key] === "");
    if (missing.length) { errors.push(`${file}: missing required fields: ${missing.join(", ")}`); continue; }
    if (entry.type !== "Time Entry") errors.push(`${file}: type must be Time Entry`);
    if (entry.task !== task.task) errors.push(`${file}: parent task mismatch`);
    if (entry.entry !== path.basename(file, ".md") || !slugPattern.test(String(entry.entry))) errors.push(`${file}: entry slug must match its filename`);
    if (!['running', 'closed'].includes(String(entry.status))) errors.push(`${file}: time status must be running or closed`);
    if (!["tracked", "tracked-adjusted", "manual", "estimated-commit-review"].includes(String(entry.method))) errors.push(`${file}: unknown time method`);
    ["started", "timestamp"].forEach((field) => { if (!rfc3339(entry[field])) errors.push(`${file}: ${field} must be an RFC 3339 datetime`); });
    ["Summary", "Basis", "Activity"].forEach((name) => { if (!heading(parsed.body, name)) errors.push(`${file}: missing required heading`); });
    if (entry.status === "running") {
      if (entry.method !== "tracked") errors.push(`${file}: running entries must use method tracked`);
      ["finished", "elapsed_minutes", "effort_minutes"].forEach((field) => { if (field in entry) errors.push(`${file}: running entry must not contain ${field}`); });
      const key = `${entry.actor}\u0000${entry.workstream ?? ""}`;
      if (running.has(key)) errors.push(`${file}: duplicate running actor/workstream`); else running.set(key, file);
    } else {
      if (entry.finished === undefined) errors.push(`${file}: closed entry requires finished`);
      if (entry.effort_minutes === undefined) errors.push(`${file}: closed entry requires effort_minutes`);
      if (entry.effort_minutes !== undefined && !nonNegativeInteger(entry.effort_minutes)) errors.push(`${file}: effort_minutes must be a non-negative integer`);
    }
  }
  if (!entries.length) {
    if (task.started) errors.push(`${taskFile}: started requires at least one time entry`);
    if (task.effort_minutes !== undefined && task.effort_minutes !== 0) errors.push(`${taskFile}: effort_minutes requires closed time entries`);
    if (task.status === "done" && !task.finished) errors.push(`${taskFile}: done task requires finished`);
    return;
  }
  const closedEffort = entries.filter((entry) => entry.status === "closed" && Number.isInteger(entry.effort_minutes)).reduce((sum, entry) => sum + Number(entry.effort_minutes), 0);
  if (task.effort_minutes !== closedEffort) errors.push(`${taskFile}: effort_minutes must equal the closed time-entry sum (${closedEffort})`);
  if (task.status === "done" && entries.some((entry) => entry.status === "running")) errors.push(`${taskFile}: done task has running time entries`);
}

export function validateBundle(bundle: string): string[] {
  const errors: string[] = [];
  if (!fs.existsSync(bundle)) return [`${bundle}: bundle does not exist`];
  for (const file of markdownFiles(bundle)) {
    if (["index.md", "log.md"].includes(path.basename(file))) continue;
    try { if (!parseDocument(file).metadata.type) errors.push(`${file}: non-reserved Markdown concept requires a non-empty type`); }
    catch (error) { errors.push(String((error as Error).message)); }
  }
  const taskFiles = fs.readdirSync(bundle, { withFileTypes: true }).filter((entry) => entry.isDirectory() && fs.existsSync(path.join(bundle, entry.name, "task.md"))).map((entry) => path.join(bundle, entry.name, "task.md")).sort();
  const external = new Map<string, string>();
  const branches = new Map<string, string>();
  for (const file of taskFiles) {
    let parsed: Parsed; try { parsed = parseDocument(file); } catch { continue; }
    const task = parsed.metadata;
    const required = ["type", "task", "title", "description", "status", "created", "timestamp"];
    const missing = required.filter((key) => task[key] === undefined || task[key] === "");
    if (missing.length) { errors.push(`${file}: missing required fields: ${missing.join(", ")}`); continue; }
    if (task.type !== "Task") errors.push(`${file}: type must be Task`);
    if (task.task !== path.basename(path.dirname(file)) || !slugPattern.test(String(task.task))) errors.push(`${file}: task slug must match its directory`);
    if (!statusSet.has(String(task.status))) errors.push(`${file}: unknown status`);
    ["created", "timestamp"].forEach((field) => { if (!rfc3339(task[field])) errors.push(`${file}: ${field} must be an RFC 3339 datetime`); });
    ["Outcome", "Scope", "Acceptance", "Evidence"].forEach((name) => { if (!heading(parsed.body, name)) errors.push(`${file}: missing required heading`); });
    if (task.completion_history !== undefined) {
      if (!Array.isArray(task.completion_history)) errors.push(`${file}: completion_history must be a list`);
      else task.completion_history.forEach((event, index) => { if (!mapping(event) || !rfc3339(event.finished) || !rfc3339(event.reopened)) errors.push(`${file}: completion_history[${index}] requires finished and reopened RFC 3339 datetimes`); });
    }
    validateEstimate(file, task, errors); validateSync(file, task, errors); validateTime(file, task, errors);
    if (Array.isArray(task.external)) task.external.forEach((item) => {
      if (!mapping(item) || !item.system || item.id === undefined) return;
      const key = `${item.system}:${item.id}`; if (external.has(key)) errors.push(`${file}: external mapping ${key} also used by ${external.get(key)}`); else external.set(key, file);
    });
    const workstreamDir = path.join(path.dirname(file), "workstreams");
    const workstreamFiles = fs.existsSync(workstreamDir) ? fs.readdirSync(workstreamDir).filter((name) => name.endsWith(".md")).map((name) => path.join(workstreamDir, name)).sort() : [];
    for (const workstreamFile of workstreamFiles) {
      let wsParsed: Parsed; try { wsParsed = parseDocument(workstreamFile); } catch { continue; }
      const ws = wsParsed.metadata;
      const wsRequired = ["type", "task", "workstream", "title", "description", "status", "created", "timestamp"];
      const wsMissing = wsRequired.filter((key) => ws[key] === undefined || ws[key] === "");
      if (wsMissing.length) { errors.push(`${workstreamFile}: missing required fields: ${wsMissing.join(", ")}`); continue; }
      if (ws.task !== task.task) errors.push(`${workstreamFile}: parent task mismatch`);
      if (ws.workstream !== path.basename(workstreamFile, ".md") || !slugPattern.test(String(ws.workstream))) errors.push(`${workstreamFile}: workstream slug must match`);
      if (!statusSet.has(String(ws.status))) errors.push(`${workstreamFile}: unknown status`);
      ["created", "timestamp"].forEach((field) => { if (!rfc3339(ws[field])) errors.push(`${workstreamFile}: ${field} must be RFC 3339`); });
      ["Assigned outcome", "Acceptance and validation", "Evidence", "Handoff"].forEach((name) => { if (!heading(wsParsed.body, name)) errors.push(`${workstreamFile}: missing required heading`); });
      if (ws.branch && !terminal.has(String(ws.status))) { const branch = String(ws.branch); if (branches.has(branch)) errors.push(`${workstreamFile}: active branch also used by ${branches.get(branch)}`); else branches.set(branch, workstreamFile); }
    }
    if (task.status === "done" && workstreamFiles.some((wsFile) => { try { return !terminal.has(String(parseDocument(wsFile).metadata.status)); } catch { return false; } })) errors.push(`${file}: done task has active workstreams`);
  }
  const index = path.join(bundle, "index.md");
  if (!fs.existsSync(index)) errors.push(`${index}: generated index is missing`);
  else if (!fs.readFileSync(index, "utf8").includes("<!-- Generated by okf-task-lifecycle. Do not edit by hand. -->")) errors.push(`${index}: generated index is stale`);
  return errors;
}
