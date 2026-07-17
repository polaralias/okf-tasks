---
type: Task
task: fixture-task
title: Fixture task
description: Exercise one portable task conformance rule.
status: ready
created: '2026-07-17T09:00:00Z'
timestamp: '2026-07-17T09:00:00Z'
owner: agent
assignees:
- agent
- reviewer
priority: high
tags:
- spec
estimate:
  effort_minutes: 180
  method: agent
  confidence: medium
  basis: Compared with similar work.
  actor: agent
  timestamp: '2026-07-17T09:00:00Z'
sprint_points:
  value: 3
  scale: fibonacci
  context: platform
  timestamp: '2026-07-17T09:00:00Z'
external:
- system: linear
  id: ENG-1
  url: https://linear.app/example/ENG-1
sync:
  authority: repository
  field_authority:
    status: tracker
  base:
    local_revision: abc
    remote_revision: '7'
producer_extension:
  preserve: true
---

# Fixture task

## Outcome

Produce the stated outcome.

## Scope

- Included: the fixture contract.

## Acceptance

- [ ] The fixture is evaluated.

## Evidence

- Conformance fixture.
