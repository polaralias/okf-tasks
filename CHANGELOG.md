# Changelog

All notable changes to OKF Tasks are recorded here.

## Unreleased

- Define stable, fragment-addressable time entries in Task frontmatter across CLI mutation, validation, schemas, graph payloads, examples, and bundled skills.

- Add an installable `okf-tasks` console command for the reference lifecycle CLI.
- Generate the visualization, relationship review, and complete examples browser from one reproducible, checkable script.
- Make `timestamp` explicitly mean the portable last meaningful change across tasks, workstreams, skills, and viewer summaries; embedded time mutations advance their Task timestamp.
- Consolidate the bundled lifecycle skill metadata, visual review guidance, and upstream RKE parity around derived OKF Visualization concepts.
- Adopt the definitive light-first Graph, Board, and Reader workspace with a visible relationship mesh, selection focus, shared record previews, workstream effort context, GitHub-style Markdown and Mermaid, temporal comparison and cautious drift hints, searchable full-width reading, and embedded Task time evidence.

## 0.4.0 — 2026-07-18

- Replace unscoped `(system, id)` mappings with host-scoped, provider-global external identities.
- Add reusable Tracker Profile concepts with explicit direction, authority, status, field, and managed-label policies.
- Add live and snapshot-based initialization for GitHub, GitLab, Linear, and ClickUp plus inspection and drift-safe refresh commands.
- Move reconciliation state from the task to each external binding and add portable typed custom fields.
- Extend both independent validators, schemas, normative fixtures, examples, security rules, and agent execution boundaries.
- Add project-local default Tracker Profiles, safe fallback selection, setup evidence in generated profiles, and documented live integration evidence.

## 0.3.0 — 2026-07-17

- Define `tasks/` as the default operational placement.
- Add `docs/tasks/` as an optional placement for repositories whose documentation tree already owns actual project delivery material.
- Add `init-bundle --placement docs` while preserving custom `--bundle` support.
- Add project-documentation example and conformance coverage.

## 0.2.0 — 2026-07-17

- Define untrusted external content and prompt injection as an adapter trust-boundary concern.
- Require deterministic inspection of exact outbound payloads for secrets, local paths, unsafe links, and explicit data policy.
- Define credential-free GitHub and GitLab conversion for repository-local Markdown links.
- Add `prepare-export` with fail-closed secret/path checks, immutable-link defaults, and provenance.
- Add thirteen shared external-artifact conformance cases to both maintained implementations.

## 0.1.0 — 2026-07-17

- Publish the OKF Tasks v0.1 profile and versioned schemas.
- Define tasks, required workstreams, lifecycle transitions, reopening history, time entries, estimates, and sprint points.
- Define repository/tracker authority, field overrides, reconciliation conflicts, and bundle-unique external mappings.
- Publish the `okf-task-lifecycle` skill and Python producer/validator.
- Add standalone, knowledge-linked, and tracker-synchronised examples.
- Add a shared conformance manifest, exhaustive transition matrix, and independent TypeScript validator.
- Add maintainer governance, protected-branch policy, and automated release gates.
