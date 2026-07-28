---
type: "Release History"
title: "Changelog"
description: "Documents Changelog for the okf-tasks repository."
timestamp: 2026-07-28T21:55:36Z
authority: evidence
verification: verified-limited
owner: polaralias
tags:
  - okf-tasks
  - release-history
navigation:
  role: reference
  order: 200
---
# Changelog

All notable changes to OKF Tasks are recorded here.

## 0.1.0 — 2026-07-19

- Publish the foundational OKF Tasks v0.1 profile, versioned schemas, and installable `okf-tasks` command.
- Define tasks, required workstreams, lifecycle transitions, reopening history, time entries, estimates, and sprint points.
- Define stable, fragment-addressable time entries in Task frontmatter and make `timestamp` the portable last meaningful change.
- Define repository/tracker authority, field overrides, reconciliation conflicts, and host-scoped external identities for GitHub, GitLab, Linear, and ClickUp.
- Add reusable Tracker Profiles, live and snapshot-based initialisation, project-local defaults, safe selection, setup evidence, and drift-safe refresh.
- Require deterministic inspection of outbound artefacts across trust boundaries, including secrets, local paths, unsafe links, and explicit data policy.
- Support both `tasks/` and project-owned `docs/tasks/` placements.
- Require tasks and durable knowledge concepts to form one resolved repository-local link graph while excluding volatile operational and generated material.
- Add a reproducible Visualisation consumer with Graph, Board, Reader, Mermaid, temporal comparison, cautious drift hints, embedded Task time evidence, reading prominence, and first-reading order.
- Publish standalone, knowledge-linked, tracker-synchronised, task-heavy, architecture-heavy, and combined examples.
- Publish the `okf-task-lifecycle` skill, Python producer/validator, independent TypeScript validator, normative fixtures, governance, and automated release gates.
- Stabilise CLI help and version output as `okf-tasks`, clarify ambiguous command and effort-estimation options, and report commit matches against the selected range.
- Add validation coverage counts, visible warning totals, `--strict` warning gates, and warnings for recognisable unedited task skeleton text.
- Require resolved dependencies during task creation unless partial-bundle mode is explicit, and keep concise descriptions separate from detailed Outcome prompts.
- Make commit backfill reruns explicitly idempotent and ignore editable-install `egg-info` metadata.
- Discover ClickUp Workspace and Space identities separately, resolve custom task IDs with the required Workspace query, and clarify invalid-ID errors.
- Allow tracker creation and push without a Git remote when the rendered body has no repository-local links; provide actionable remote options when links require repository context.

## Repository knowledge

- [Documentation map](docs/knowledge/documentation-map.md) — RKE-managed reading order and relationship hub.
