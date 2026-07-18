---
type: Task
task: add-audit-events
title: Add authentication audit events
description: Emit structured audit events for successful and failed authentication attempts.
status: in-progress
created: 2026-07-17T09:00:00Z
timestamp: 2026-07-17T20:20:00Z
started: 2026-07-17T07:45:00Z
effort_minutes: 180
estimate:
  effort_minutes: 240
  method: agent
  confidence: medium
  basis: Event schema, implementation, tests, review feedback, and audit-pipeline validation.
  actor: planning-agent
  timestamp: 2026-07-17T07:30:00Z
sprint_points:
  value: 5
  scale: fibonacci
  context: security-team
  timestamp: 2026-07-17T07:30:00Z
owner: security-team
external:
  - tracker: linear-security
    system: linear
    host: https://api.linear.app
    kind: issue
    scope:
      id: 6c02a067-25da-4f67-b2e3-c0aa3217f01a
      key: SEC
    id: 1edc92a8-bb50-46f1-ae17-b7bd05c8bfdf
    key: SEC-142
    url: https://linear.app/example/issue/SEC-142
    sync:
      last_synced: 2026-07-17T12:00:00Z
      remote_revision: 2026-07-17T11:55:00Z
      base:
        local: sha256:task-revision-17
        remote: sha256:linear-revision-17
---

# Add authentication audit events

## Outcome

Security operators can distinguish successful and failed authentication attempts using structured audit events.

## Scope

- In scope: service-side authentication outcomes.
- Out of scope: browser telemetry.

## Acceptance

- [ ] Emit success and failure event variants.
- [ ] Redact credentials and session secrets.
- [ ] Verify events in the audit pipeline.

## Dependencies and risks

- Audit event schema review is pending.

## Related knowledge

- Link the approved audit schema when available.

## Workstreams

- No separate workstreams.

## Evidence

- Implementation is active; no completion evidence yet.
- Effort: commit review found two plausible 90-minute work sessions across a 12.5-hour evidence window.
