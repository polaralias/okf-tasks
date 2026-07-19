# OKF Tasks visualization example

> Generated from repository-local OKF records. The Markdown/YAML bundle remains canonical.

Source: `examples/visualization/tasks`

The report separates the connected repository map from detailed component and key-concept views so large bundles remain reviewable.

## Connected-area overview

```mermaid
flowchart LR
    a0["publish-guide · 1 concepts"]
    a1["release-okf-tasks · 3 concepts"]
    a0 -->|depends on| a1
    classDef default fill:#eef2ff,stroke:#4f46e5,color:#1e1b4b
```

## Connected component 1

```mermaid
flowchart LR
    n0["Publish the visualization guide · proposed"]:::task
    n1["Release OKF Tasks · in-progress"]:::task
    n2["Specification and conformance · validation"]:::workstream
    n3["Visualization consumer · in-progress"]:::workstream
    n0 -->|depends on| n1
    n1 -->|time:visualization-session| n1
    n2 -->|workstream| n1
    n3 -->|workstream| n1
    classDef task fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef workstream fill:#ede9fe,stroke:#7c3aed,color:#2e1065
    classDef tracker fill:#ffedd5,stroke:#ea580c,color:#431407
    classDef knowledge fill:#dcfce7,stroke:#16a34a,color:#052e16
    classDef boundary fill:#f8fafc,stroke:#64748b,color:#0f172a,stroke-dasharray:4 3
```

## Key concept neighbourhoods

### Release OKF Tasks

```mermaid
flowchart LR
    n0["Publish the visualization guide · proposed"]:::boundary
    n1["Release OKF Tasks · in-progress"]:::task
    n2["Specification and conformance · validation"]:::boundary
    n3["Visualization consumer · in-progress"]:::boundary
    n0 -->|depends on| n1
    n1 -->|time:visualization-session| n1
    n2 -->|workstream| n1
    n3 -->|workstream| n1
    classDef task fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef workstream fill:#ede9fe,stroke:#7c3aed,color:#2e1065
    classDef tracker fill:#ffedd5,stroke:#ea580c,color:#431407
    classDef knowledge fill:#dcfce7,stroke:#16a34a,color:#052e16
    classDef boundary fill:#f8fafc,stroke:#64748b,color:#0f172a,stroke-dasharray:4 3
```

## Unconnected concepts

These records are listed instead of receiving equal visual weight in the connected graph.

- **trackers/github-main** — `trackers/github-main` (Tracker Profile)

## Legend

- Blue: task
- Purple: workstream
- Orange: tracker profile
- Green: durable knowledge
- Dashed neutral nodes: neighbouring context repeated from another area or key-concept view
- Time references: edges to addressable `Task.time[]` fragments
- Arrows: structured relationships or repository-local Markdown links
