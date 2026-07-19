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
