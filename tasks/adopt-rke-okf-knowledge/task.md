---
type: Task
task: adopt-rke-okf-knowledge
title: Adopt RKE OKF knowledge format
description: Represent durable repository knowledge and migration evidence in the
  full RKE OKF format.
status: done
created: '2026-07-28T21:57:07Z'
timestamp: '2026-07-28T23:11:09Z'
owner: polaralias
time:
- id: 20260728t215708z-codex-tracked
  status: closed
  actor: codex
  started: '2026-07-28T21:57:08Z'
  method: tracked-adjusted
  activity: knowledge-maintenance
  summary: Adjusted allocation from one shared cross-repository migration and validation
    session; prevents duplicate portfolio effort.
  basis: 'Wall-clock session was 19 minutes. Active effort was adjusted to 2 minutes:
    Adjusted allocation from one shared cross-repository migration and validation
    session; prevents duplicate portfolio effort.'
  finished: '2026-07-28T22:16:17Z'
  elapsed_minutes: 19
  effort_minutes: 2
- id: 20260728t223502z-codex-tracked
  status: closed
  actor: codex
  started: '2026-07-28T22:35:02Z'
  method: tracked-adjusted
  activity: knowledge-maintenance
  summary: Adjusted allocation from one shared branch-rename, duplicate-removal, and
    exhaustive Markdown census session.
  basis: 'Wall-clock session was 4 minutes. Active effort was adjusted to 2 minutes:
    Adjusted allocation from one shared branch-rename, duplicate-removal, and exhaustive
    Markdown census session.'
  finished: '2026-07-28T22:38:59Z'
  elapsed_minutes: 4
  effort_minutes: 2
- id: 20260728t224136z-codex-tracked
  status: closed
  actor: codex
  started: '2026-07-28T22:41:36Z'
  method: tracked-adjusted
  activity: knowledge-maintenance
  summary: Applied and verified the skill-package Markdown exclusion in the exhaustive
    repository census.
  basis: 'Wall-clock session was 9 minutes. Active effort was adjusted to 1 minutes:
    Applied and verified the skill-package Markdown exclusion in the exhaustive repository
    census.'
  finished: '2026-07-28T22:50:25Z'
  elapsed_minutes: 9
  effort_minutes: 1
- id: 20260728t225559z-codex-tracked
  status: closed
  actor: codex
  started: '2026-07-28T22:55:59Z'
  method: tracked-adjusted
  activity: knowledge-maintenance
  summary: Generated, integrated, and validated repository-wide HTML and Mermaid OKF
    visualizations.
  basis: 'Wall-clock session was 15 minutes. Active effort was adjusted to 1 minutes:
    Generated, integrated, and validated repository-wide HTML and Mermaid OKF visualizations.'
  finished: '2026-07-28T23:11:07Z'
  elapsed_minutes: 15
  effort_minutes: 1
started: '2026-07-28T21:57:08Z'
effort_minutes: 6
completion_history:
- finished: '2026-07-28T22:17:39Z'
  reopened: '2026-07-28T22:35:02Z'
- finished: '2026-07-28T22:39:31Z'
  reopened: '2026-07-28T22:41:35Z'
- finished: '2026-07-28T22:50:27Z'
  reopened: '2026-07-28T22:55:59Z'
finished: '2026-07-28T23:11:09Z'
---

# Adopt RKE OKF knowledge format

## Outcome

Durable repository knowledge is represented with portable, plaintext OKF metadata, connected through an RKE-managed relationship graph, and kept distinct from operational Task state and specialised producer-owned schemas.

## Scope

- In scope: type and connect 10 durable knowledge documents; create and validate the bounded `docs/knowledge/` bundle; record this migration as an OKF Task; generate repository-wide HTML and Mermaid views.
- In scope: preserve canonical, evidence, derived, generated, instruction, handoff, fixture, and task boundaries.
- Out of scope: change product behaviour, upgrade support claims, rewrite historical evidence, publish externally, or alter generated/vendor content outside its owning workflow.

## Acceptance

- [x] Classify durable documents and deliberate schema exclusions.
- [x] Add required and recommended plaintext RKE OKF metadata.
- [x] Connect governed knowledge and execution concepts through repository-relative links.
- [x] Preserve reserved indexes and specialised document schemas.
- [x] Classify all 401 in-scope repository Markdown files with zero omissions; exclude 4 skill-package documents.
- [x] Remove the redundant repository overview and confirm zero exact duplicate governed knowledge bodies.
- [x] Build and validate the `docs/knowledge/` bundle.
- [x] Validate the migration Task structurally; repository-wide strict graph validation is limited by deliberately isolated example and conformance workspaces.
- [x] Confirm the RKE-compatible upstream skill remains feature-identical and release-valid.

## Dependencies and risks

- The installed `okf-tasks 0.1.0` package is missing its task-body asset; the feature-identical bundled reference CLI is used instead.
- Metadata migration does not upgrade the evidential strength of existing repository claims.
- Existing manual indexes, generated documents, handoffs, fixtures, and skill packages retain their owning formats.

## Related knowledge

- [Documentation map](../../docs/knowledge/documentation-map.md)
- [Repository visualization](../../docs/knowledge/repository-visualization.md)

## Workstreams

- No separately owned workstreams are required.

## Evidence

- RKE bundle validation: conformant (3 concepts, 1 generated index).
- Migration Task validation: structurally conformant; repository-aware graph validation reports only deliberate fixture/workspace separation.
- Canonical release bar: 75 Python tests and 61 TypeScript conformance tests passed; fixture, npm audit, and release metadata checks passed.
- Upstream lifecycle parity: specification semantics remain feature-identical; skill-package documents retain their own schema and require no RKE wrapper or package-version change.
- Complete Markdown census: 401 in-scope files, 4 skill-package files excluded, 0 unclassified, 0 exact duplicate governed knowledge bodies. Repeated examples and conformance fixtures remain producer-owned boundaries.
