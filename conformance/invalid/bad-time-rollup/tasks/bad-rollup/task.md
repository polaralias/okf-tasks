---
type: Task
task: bad-rollup
title: Bad time rollup
description: Demonstrate rejection of a task whose effort does not match its time entries.
status: in-progress
created: 2026-07-17T09:00:00Z
timestamp: 2026-07-17T10:00:00Z
started: 2026-07-17T09:00:00Z
effort_minutes: 120
---

# Bad time rollup

## Outcome

This fixture must fail validation.

## Scope

- In scope: time rollup validation.

## Acceptance

- [ ] Validation fails.

## Evidence

- The task claims 120 minutes while its entry records 60.
