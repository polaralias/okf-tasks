---
type: "Repository Knowledge"
title: "Tracker integration setup and live evidence"
description: "Documents Tracker integration setup and live evidence for the okf-tasks repository."
timestamp: 2026-10-19T16:30:00Z
authority: canonical
verification: untested
owner: polaralias
tags:
  - okf-tasks
  - repository-knowledge
navigation:
  role: supporting
  order: 100
---
# Tracker integration setup and live evidence

This document records how OKF Tasks establishes a first-class tracker connection and the live verification performed for the provider layer included in the foundational v0.1 release. It intentionally contains no credentials or credential references.

## Project setup process

1. Identify the repository-local task bundle and inspect existing Tracker Profiles under `tasks/trackers/`.
2. Discover the provider surface appropriate to the current project:
   - GitHub repository;
   - GitLab project and host;
   - Linear team;
   - ClickUp List, including its Workspace context.
3. If more than one surface is plausible, present the candidates and ask the user which project scope should receive new tasks. Do not infer a writable destination merely from account access.
4. Initialise the selected scope from live discovery. Review proposed status mappings, provider capabilities, custom fields, and managed-label ownership.
5. Save the selected profile as the project default with `tracker init --default` or `tracker set-default`. The default is repository data; authentication remains runtime-only.
6. Create, import, or synchronise. Provider writes are read back before the reconciliation base advances.
7. Re-run `tracker refresh` when provider configuration changes, and retain validation or live-test evidence with the delivery change.

```text
okf-tasks tracker init --root . --tracker linear-engineering --system linear --scope ENG --mode bidirectional --authority repository --default
okf-tasks tracker set-default --root . --tracker linear-engineering
okf-tasks tracker create --root . --task new-task
okf-tasks tracker sync --root . --task new-task --direction push
```

An explicit `--tracker` always wins. Without one, the CLI uses the saved default, then a sole profile. If several profiles exist without one safe default, it stops and lists the available profiles so the user can choose and save one.

## Credential boundary

Credentials were supplied only through runtime environment variables: `GITHUB_TOKEN`, `GITLAB_TOKEN`, `LINEAR_API_KEY`, and `CLICKUP_API_TOKEN`. Self-managed GitLab can use a runtime certificate trust path and `--api-base`. Profiles store the provider host, stable scope identity, discovery fingerprint, mappings, and setup evidence, but never a token, secret, credential reference, or machine-local certificate path.

## Live verification — 2026-07-18

| Provider | Surface | Verified behaviour | Cleanup |
|---|---|---|---|
| GitHub | `polaralias/agentic-workflow-testing` repository | Discovery, profile validation and refresh, issue create/read-back, push, remote-revision conflict refusal, import, and managed-label preservation | Test issues closed; temporary labels removed; no open issues |
| Linear | `POL` team in the Polaralias testing workspace | Team and workflow discovery, issue create/read-back, push, conflict refusal, unique reverse-status pull, and import | Test issues archived |
| ClickUp | Disposable List in the testing Workspace | List discovery, profile validation and refresh, task create/read-back, push, conflict refusal, and import | Disposable List and tasks deleted |
| GitLab | Disposable GitLab CE 19.2.0 project served locally over HTTPS | Project discovery, profile validation and refresh, issue create/read-back, push, conflict refusal, import, inspection, and managed-label preservation | Container, project, certificate, token, test files, and image removed |

GitHub and GitLab both preserved a foreign `human-review` label while updating the OKF-owned `okf:` subset. Linear's discovered `Todo` state mapped uniquely back to `ready`. GitHub, GitLab, and ClickUp correctly refused ambiguous reverse mappings where several OKF states collapse into a provider's open state.

GitHub validation also distinguishes rich issue bodies from structured fields. GitHub Flavoured Markdown renders emphasis and labelled links in issue bodies and Markdown files, while organisation Issue Fields are typed metadata; GitHub documents text fields as free-form text whose bare URLs are automatically detected and made clickable. OKF therefore keeps all frontmatter string values presentation-free for portable title, label, custom-field, and provider synchronisation. Bare URLs and repository references are valid; Markdown or HTML formatting belongs in the body.

The live scopes did not expose writable arbitrary custom fields suitable for a safe create/read-back test. ClickUp returned zero accessible List custom fields; the GitHub, GitLab, and Linear test surfaces likewise did not provide a writable arbitrary issue-field transport. Stable custom-field identifiers and outbound value construction remain covered by the machine test suite.

## Verification evidence

- Python reference implementation: 34 tests passed during the original provider run; the expanded default-selection suite is part of the current release bar.
- Independent TypeScript validator: all manifest cases passed.
- Generated fixtures were current.
- Release metadata was consistent for v0.1.0.
- Live credentials were cleared after use and no test credential was persisted in either repository.

## Repository knowledge

- [Documentation map](knowledge/documentation-map.md) — RKE-managed reading order and relationship hub.

## Many-to-many contributions — profile 0.2

Connections and field ownership are distinct. `reference` records observations only; `mirror` retains the existing replication contract; `contribution` publishes independently managed work to one combined remote progress section. Omitted relationships remain mirrors. A local task may have several remotes in one profile, and several local tasks may contribute to the same remote. The local-task/remote pair remains unique, including across aliases. Shared writers must use one profile; mirror and contribution writers cannot coexist for one remote.

Migration is explicit and local:

```text
okf-tasks inspect-external --root . --task implement-api
okf-tasks unlink-external --root . --task implement-api --remote-id <raw-task-id> --relationship contribution
okf-tasks link-external --root . --task test-api --id <raw-task-id> --key AI-952 --url https://app.clickup.com/t/<raw-task-id> --relationship contribution
okf-tasks tracker sync --root . --task implement-api --direction push --remote-id <raw-task-id>
```

Select the intended profile with `--tracker` when there is no saved/sole default. A bulk sync uses `--all-bindings`; it returns a result per binding and a nonzero exit if any target fails. Successful targets retain their verified success state. No rollback of completed provider requests is implied.

Contribution summaries contain local slugs, titles and lifecycle statuses in deterministic order. They do not publish private local bodies or acceptance sections. Shared remote status remains manual. Pull records observations without completing, reopening or rewriting contributors. Reference or contribution imports start `proposed` unless an explicit local status is supplied. A mirror pull with several possible mirror sources requires one binding `sync.pull_source: true`.

The publisher preserves human text outside its owned section and refuses edited, duplicated, malformed or foreign ownership markers. It checks the exact outgoing description for secrets and nonportable links, validates identity and current scope, rechecks the remote revision immediately before writing, and verifies the complete description afterward. Field conflicts in the owned section cannot be bypassed with `--force`. A timeout retains pending evidence without advancing success; retry can recognise the exact attempted section. Providers do not offer a common atomic conditional-update contract: human edits between the final read and write remain a provider-level race. Local locks coordinate cooperating commands only; remote/distributed atomicity is not claimed.

Task external entries are canonical membership. Keep `<bundle>/.tracker-sync/` JSON ownership/base records with the bundle when moving or distributing it. State is keyed by the complete provider identity and stores a random owner, section hash, membership fingerprint, remote revision, timestamps, and optional pending hash. Missing state refuses to adopt an existing summary. Do not put credentials in these records. A `.tracker.lock` is a transient exclusive lock: recover it only after verifying the owning process has stopped.

`unlink-external` removes only the local relationship, or converts it when `--relationship` is supplied. A remaining contributor's next push recomputes membership; removing the final contributor retains the last remote summary for explicit human removal. No local or remote task is deleted. Cross-repository aggregation, automatic status roll-up, webhooks and remote task restructuring are outside this version.

The adapter enforces configured direction and repository push authority. Whole-record mirror transport refuses mixed field authorities rather than silently overriding them. Mirrors retain conservative whole-record revision conflict detection; contribution conflicts are scoped to the managed description section.

Upgrade all consuming validators and writers before introducing shared records. Older validators reject the cardinality, and older writers lack contribution ownership semantics. The 0.2 schema/specification identity supersedes 0.1 for these records; it does not make an old installed writer safe.

Verification for this change uses local provider mocks and independent conformance validators. The historical live tests above do not establish live many-to-many behaviour.
