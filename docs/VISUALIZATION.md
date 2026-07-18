# OKF Tasks visualization example

> Generated from repository-local OKF records. The Markdown/YAML bundle remains canonical.

Source: `examples/visualization/tasks`

```mermaid
flowchart LR
    n0["Publish the visualization guide · proposed"]:::task
    n1["Release OKF Tasks · in-progress"]:::task
    n2["visualization-session · closed"]:::time_entry
    n3["Specification and conformance · validation"]:::workstream
    n4["Visualization consumer · in-progress"]:::workstream
    n0 -->|depends on| n1
    n1 -->|links| n2
    n2 -->|time| n4
    n3 -->|workstream| n1
    n4 -->|workstream| n1
    classDef task fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef workstream fill:#ede9fe,stroke:#7c3aed,color:#2e1065
    classDef time_entry fill:#d1fae5,stroke:#059669,color:#022c22
    classDef unknown fill:#e2e8f0,stroke:#64748b,color:#0f172a
```

## Legend

- Blue: task
- Purple: workstream
- Green: time entry
- Arrows: structured relationships or repository-local Markdown links
