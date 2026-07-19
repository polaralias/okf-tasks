# OKF Tasks visualization example

> Generated from repository-local OKF records. The Markdown/YAML bundle remains canonical.

Source: `examples/visualization/tasks`

```mermaid
flowchart LR
    n0["Publish the visualization guide · proposed"]:::task
    n1["Release OKF Tasks · in-progress"]:::task
    n2["Specification and conformance · validation"]:::workstream
    n3["Visualization consumer · in-progress"]:::workstream
    n4["trackers/github-main"]:::unknown
    n0 -->|depends on| n1
    n1 -->|time:visualization-session| n1
    n2 -->|workstream| n1
    n3 -->|workstream| n1
    classDef task fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef workstream fill:#ede9fe,stroke:#7c3aed,color:#2e1065
    classDef unknown fill:#e2e8f0,stroke:#64748b,color:#0f172a
```

## Legend

- Blue: task
- Purple: workstream
- Time references: edges to addressable `Task.time[]` fragments
- Arrows: structured relationships or repository-local Markdown links
