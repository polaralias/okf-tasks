# OKF combined delivery and architecture workspace

> Generated from repository-local OKF records. The Markdown/YAML bundle remains canonical.

Source: `examples/combined-delivery-architecture`

The report separates the connected repository map from detailed component and key-concept views so large bundles remain reviewable.

## Connected-area overview

```mermaid
flowchart LR
    a0["docs · 57 concepts"]
    a1["repository root · 1 concepts"]
    a2["tasks · 51 concepts"]
    a0 -->|links| a2
    a1 -->|links| a0
    a2 -->|links| a0
    classDef default fill:#eef2ff,stroke:#4f46e5,color:#1e1b4b
```

## Connected component 1

### docs

```mermaid
flowchart LR
    n0["Container Topology · current"]:::knowledge
    n1["Data Platform · current"]:::knowledge
    n2["Deployment Topology · current"]:::knowledge
    n3["Event Backbone · current"]:::knowledge
    n4["Identity Boundary · current"]:::knowledge
    n5["Migration Architecture · current"]:::knowledge
    n6["Observability Model · current"]:::knowledge
    n7["Request Lifecycle · current"]:::knowledge
    n8["Resilience Model · current"]:::knowledge
    n9["Security Architecture · current"]:::knowledge
    n10["System Context · current"]:::knowledge
    n11["Tenant Isolation · current"]:::knowledge
    n12["Customer Experience delivery plan · current"]:::knowledge
    n13["Data Migration delivery plan · current"]:::knowledge
    n14["Adr 001: Modular Service Boundaries · accepted"]:::knowledge
    n15["Adr 002: Versioned Event Envelope · accepted"]:::knowledge
    n16["Adr 003: Oidc Workload Identity · accepted"]:::knowledge
    n17["Adr 004: Tenant Key Partitioning · accepted"]:::knowledge
    n18["Adr 005: Transactional Outbox · accepted"]:::knowledge
    n19["Adr 006: Idempotent Command Handling · accepted"]:::knowledge
    n20["Adr 007: Schema Registry Compatibility · accepted"]:::knowledge
    n21["Adr 008: Zero Downtime Database Change · accepted"]:::knowledge
    n22["Adr 009: Regional Active Passive · accepted"]:::knowledge
    n23["Adr 010: Central Policy Evaluation · accepted"]:::knowledge
    n24["Adr 011: Short Lived Access Tokens · accepted"]:::knowledge
    n25["Adr 012: Immutable Deployment Artefacts · accepted"]:::knowledge
    n26["Adr 013: Progressive Delivery · accepted"]:::knowledge
    n27["Adr 014: Open Telemetry Signals · accepted"]:::knowledge
    n28["Adr 015: Error Budget Release Gates · accepted"]:::knowledge
    n29["Adr 016: Encrypted Event Payloads · accepted"]:::knowledge
    n30["Adr 017: Customer Managed Retention · accepted"]:::knowledge
    n31["Adr 018: Migration Dual Read Window · proposed"]:::knowledge
    n32["Adr 019: Bounded Retry Policies · proposed"]:::knowledge
    n33["Adr 020: Architecture Evidence Records · proposed"]:::knowledge
    n34["Identity Security delivery plan · current"]:::knowledge
    n35["Audit Event Contract · current"]:::knowledge
    n36["Customer Events · current"]:::knowledge
    n37["Identity Events · current"]:::knowledge
    n38["Migration Control Api · current"]:::knowledge
    n39["Public Api · current"]:::knowledge
    n40["Reporting Query Api · current"]:::knowledge
    n41["Observability Release delivery plan · current"]:::knowledge
    n42["Platform Foundations delivery plan · current"]:::knowledge
    n43["Programme Delivery And Architecture Map · current"]:::knowledge
    n44["Availability · current"]:::knowledge
    n45["Operability · current"]:::knowledge
    n46["Performance · current"]:::knowledge
    n47["Recoverability · current"]:::knowledge
    n48["Security · current"]:::knowledge
    n49["Audit Service · current"]:::knowledge
    n50["Customer Service · current"]:::knowledge
    n51["Identity Service · current"]:::knowledge
    n52["Migration Service · current"]:::knowledge
    n53["Notification Service · current"]:::knowledge
    n54["Reporting Service · current"]:::knowledge
    n55["Tenant Service · current"]:::knowledge
    n56["Workflow Service · current"]:::knowledge
    n57["Combined delivery and architecture workspace"]:::boundary
    n58["Add migration progress centre · in-progress"]:::boundary
    n59["Add privileged access reviews · validation"]:::boundary
    n60["Add release health checks · in-progress"]:::boundary
    n61["Approve architecture readiness · blocked"]:::boundary
    n62["Approve general availability · ready"]:::boundary
    n63["Approve production cutover data · ready"]:::boundary
    n64["Automate dependency updates · blocked"]:::boundary
    n65["Benchmark critical request paths · ready"]:::boundary
    n66["Build account creation flow · done"]:::boundary
    n67["Build change data capture pipeline · validation"]:::boundary
    n68["Build operational dashboards · validation"]:::boundary
    n69["Build shared authentication middleware · ready"]:::boundary
    n70["Complete guided onboarding trials · blocked"]:::boundary
    n71["Complete release rehearsal · blocked"]:::boundary
    n72["Complete threat model review · blocked"]:::boundary
    n73["Create cross-service trace model · done"]:::boundary
    n74["Create reconciliation reports · in-progress"]:::boundary
    n75["Define canonical customer schema · done"]:::boundary
    n76["Define service level objectives · done"]:::boundary
    n77["Define service ownership · done"]:::boundary
    n78["Design recoverable form states · ready"]:::boundary
    n79["Enforce workload identity · in-progress"]:::boundary
    n80["Establish repository boundaries · done"]:::boundary
    n81["Exercise rollback automation · ready"]:::boundary
    n82["Exercise tenant isolation · in-progress"]:::boundary
    n83["Harden session management · ready"]:::boundary
    n84["Implement organisation switching · validation"]:::boundary
    n85["Implement token rotation · done"]:::boundary
    n86["Instrument authentication failures · proposed"]:::boundary
    n87["Introduce feature flagging · proposed"]:::boundary
    n88["Inventory legacy data sources · done"]:::boundary
    n89["Map onboarding journey · done"]:::boundary
    n90["Meet accessibility acceptance · proposed"]:::boundary
    n91["Migrate reference data · ready"]:::boundary
    n92["Model tenant isolation · done"]:::boundary
    n93["Prototype the event backbone · validation"]:::boundary
    n94["Provision development environments · validation"]:::boundary
    n95["Publish customer experience readiness · ready"]:::boundary
    n96["Publish platform readiness evidence · ready"]:::boundary
    n97["Rehearse regional recovery · proposed"]:::boundary
    n98["Resolve migration exceptions · blocked"]:::boundary
    n99["Run customer migration rehearsal · proposed"]:::boundary
    n100["Run failure injection scenarios · proposed"]:::boundary
    n101["Standardise configuration loading · in-progress"]:::boundary
    n102["Validate architecture decision coverage · done"]:::boundary
    n103["Validate security launch controls · ready"]:::boundary
    n0 -->|links| n15
    n0 -->|links| n22
    n0 -->|links| n55
    n0 -->|links| n56
    n1 -->|links| n19
    n1 -->|links| n26
    n1 -->|links| n53
    n1 -->|links| n51
    n2 -->|links| n21
    n2 -->|links| n28
    n2 -->|links| n54
    n2 -->|links| n50
    n3 -->|links| n20
    n3 -->|links| n27
    n3 -->|links| n49
    n3 -->|links| n55
    n4 -->|links| n17
    n4 -->|links| n24
    n4 -->|links| n52
    n4 -->|links| n49
    n5 -->|links| n25
    n5 -->|links| n32
    n5 -->|links| n52
    n5 -->|links| n49
    n6 -->|links| n23
    n6 -->|links| n30
    n6 -->|links| n55
    n6 -->|links| n56
    n7 -->|links| n16
    n7 -->|links| n23
    n7 -->|links| n50
    n7 -->|links| n53
    n8 -->|links| n22
    n8 -->|links| n29
    n8 -->|links| n51
    n8 -->|links| n52
    n9 -->|links| n24
    n9 -->|links| n31
    n9 -->|links| n50
    n9 -->|links| n53
    n10 -->|links| n14
    n10 -->|links| n21
    n10 -->|links| n51
    n10 -->|links| n52
    n11 -->|links| n18
    n11 -->|links| n25
    n11 -->|links| n56
    n11 -->|links| n54
    n12 -->|links| n89
    n12 -->|links| n66
    n12 -->|links| n84
    n12 -->|links| n58
    n12 -->|links| n78
    n12 -->|links| n90
    n12 -->|links| n70
    n12 -->|links| n95
    n13 -->|links| n88
    n13 -->|links| n75
    n13 -->|links| n67
    n13 -->|links| n74
    n13 -->|links| n91
    n13 -->|links| n99
    n13 -->|links| n98
    n13 -->|links| n63
    n14 -->|links| n10
    n15 -->|links| n0
    n15 -->|links| n14
    n16 -->|links| n7
    n16 -->|links| n15
    n17 -->|links| n4
    n17 -->|links| n16
    n18 -->|links| n11
    n18 -->|links| n17
    n19 -->|links| n1
    n19 -->|links| n18
    n20 -->|links| n3
    n20 -->|links| n19
    n21 -->|links| n2
    n21 -->|links| n20
    n22 -->|links| n8
    n22 -->|links| n21
    n23 -->|links| n6
    n23 -->|links| n22
    n24 -->|links| n9
    n24 -->|links| n23
    n25 -->|links| n5
    n25 -->|links| n24
    n26 -->|links| n10
    n26 -->|links| n25
    n27 -->|links| n0
    n27 -->|links| n26
    n28 -->|links| n7
    n28 -->|links| n27
    n29 -->|links| n4
    n29 -->|links| n28
    n30 -->|links| n11
    n30 -->|links| n29
    n31 -->|links| n1
    n31 -->|links| n30
    n32 -->|links| n3
    n32 -->|links| n31
    n33 -->|links| n2
    n33 -->|links| n32
    n34 -->|links| n92
    n34 -->|links| n85
    n34 -->|links| n59
    n34 -->|links| n79
    n34 -->|links| n83
    n34 -->|links| n86
    n34 -->|links| n72
    n34 -->|links| n103
    n35 -->|links| n56
    n35 -->|links| n49
    n35 -->|links| n27
    n36 -->|links| n50
    n36 -->|links| n56
    n36 -->|links| n21
    n37 -->|links| n55
    n37 -->|links| n52
    n37 -->|links| n18
    n38 -->|links| n52
    n38 -->|links| n53
    n38 -->|links| n24
    n39 -->|links| n51
    n39 -->|links| n50
    n39 -->|links| n15
    n40 -->|links| n53
    n40 -->|links| n54
    n40 -->|links| n30
    n41 -->|links| n76
    n41 -->|links| n73
    n41 -->|links| n68
    n41 -->|links| n60
    n41 -->|links| n81
    n41 -->|links| n100
    n41 -->|links| n71
    n41 -->|links| n62
    n42 -->|links| n80
    n42 -->|links| n77
    n42 -->|links| n94
    n42 -->|links| n101
    n42 -->|links| n69
    n42 -->|links| n87
    n42 -->|links| n64
    n42 -->|links| n96
    n43 -->|links| n10
    n43 -->|links| n14
    n43 -->|links| n42
    n43 -->|links| n80
    n43 -->|links| n102
    n44 -->|links| n11
    n44 -->|links| n16
    n45 -->|links| n8
    n45 -->|links| n32
    n46 -->|links| n3
    n46 -->|links| n24
    n47 -->|links| n2
    n47 -->|links| n28
    n48 -->|links| n1
    n48 -->|links| n20
    n49 -->|links| n10
    n49 -->|links| n39
    n50 -->|links| n11
    n50 -->|links| n36
    n51 -->|links| n10
    n51 -->|links| n39
    n52 -->|links| n3
    n52 -->|links| n38
    n53 -->|links| n9
    n53 -->|links| n40
    n54 -->|links| n7
    n54 -->|links| n37
    n55 -->|links| n7
    n55 -->|links| n37
    n56 -->|links| n8
    n56 -->|links| n35
    n57 -->|links| n43
    n57 -->|links| n10
    n57 -->|links| n42
    n58 -->|links| n84
    n58 -->|links| n89
    n58 -->|links| n12
    n59 -->|links| n85
    n59 -->|links| n34
    n60 -->|links| n68
    n60 -->|links| n76
    n60 -->|links| n41
    n61 -->|links| n97
    n61 -->|links| n9
    n61 -->|links| n29
    n62 -->|links| n71
    n62 -->|links| n81
    n62 -->|links| n41
    n63 -->|links| n98
    n63 -->|links| n91
    n63 -->|links| n13
    n64 -->|links| n87
    n64 -->|links| n101
    n64 -->|links| n42
    n65 -->|links| n82
    n65 -->|links| n3
    n65 -->|links| n23
    n66 -->|links| n89
    n66 -->|links| n12
    n67 -->|links| n75
    n67 -->|links| n13
    n68 -->|links| n73
    n68 -->|links| n41
    n69 -->|links| n101
    n69 -->|links| n77
    n69 -->|links| n42
    n70 -->|links| n90
    n70 -->|links| n58
    n70 -->|links| n12
    n71 -->|links| n100
    n71 -->|links| n60
    n71 -->|links| n41
    n72 -->|links| n86
    n72 -->|links| n79
    n72 -->|links| n34
    n73 -->|links| n76
    n73 -->|links| n41
    n74 -->|links| n67
    n74 -->|links| n88
    n74 -->|links| n13
    n75 -->|links| n88
    n75 -->|links| n13
    n76 -->|links| n95
    n76 -->|links| n41
    n77 -->|links| n80
    n77 -->|links| n42
    n78 -->|links| n58
    n78 -->|links| n66
    n78 -->|links| n12
    n79 -->|links| n59
    n79 -->|links| n92
    n79 -->|links| n34
    n80 -->|links| n42
    n81 -->|links| n60
    n81 -->|links| n73
    n81 -->|links| n41
    n82 -->|links| n93
    n82 -->|links| n11
    n82 -->|links| n20
    n83 -->|links| n79
    n83 -->|links| n85
    n83 -->|links| n34
    n84 -->|links| n66
    n84 -->|links| n12
    n85 -->|links| n92
    n85 -->|links| n34
    n86 -->|links| n83
    n86 -->|links| n59
    n86 -->|links| n34
    n87 -->|links| n69
    n87 -->|links| n94
    n87 -->|links| n42
    n88 -->|links| n103
    n88 -->|links| n13
    n89 -->|links| n63
    n89 -->|links| n12
    n90 -->|links| n78
    n90 -->|links| n84
    n90 -->|links| n12
    n91 -->|links| n74
    n91 -->|links| n75
    n91 -->|links| n13
    n92 -->|links| n96
    n92 -->|links| n34
    n93 -->|links| n102
    n93 -->|links| n7
    n93 -->|links| n17
    n94 -->|links| n77
    n94 -->|links| n42
    n95 -->|links| n70
    n95 -->|links| n78
    n95 -->|links| n12
    n96 -->|links| n64
    n96 -->|links| n69
    n96 -->|links| n42
    n97 -->|links| n65
    n97 -->|links| n8
    n97 -->|links| n26
    n98 -->|links| n99
    n98 -->|links| n74
    n98 -->|links| n13
    n99 -->|links| n91
    n99 -->|links| n67
    n99 -->|links| n13
    n100 -->|links| n81
    n100 -->|links| n68
    n100 -->|links| n41
    n101 -->|links| n94
    n101 -->|links| n80
    n101 -->|links| n42
    n102 -->|links| n10
    n102 -->|links| n14
    n103 -->|links| n72
    n103 -->|links| n83
    n103 -->|links| n34
    classDef task fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef workstream fill:#ede9fe,stroke:#7c3aed,color:#2e1065
    classDef tracker fill:#ffedd5,stroke:#ea580c,color:#431407
    classDef knowledge fill:#dcfce7,stroke:#16a34a,color:#052e16
    classDef boundary fill:#f8fafc,stroke:#64748b,color:#0f172a,stroke-dasharray:4 3
```

### repository root

```mermaid
flowchart LR
    n0["System Context · current"]:::boundary
    n1["Platform Foundations delivery plan · current"]:::boundary
    n2["Programme Delivery And Architecture Map · current"]:::boundary
    n3["Combined delivery and architecture workspace"]:::knowledge
    n2 -->|links| n0
    n2 -->|links| n1
    n3 -->|links| n2
    n3 -->|links| n0
    n3 -->|links| n1
    classDef task fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef workstream fill:#ede9fe,stroke:#7c3aed,color:#2e1065
    classDef tracker fill:#ffedd5,stroke:#ea580c,color:#431407
    classDef knowledge fill:#dcfce7,stroke:#16a34a,color:#052e16
    classDef boundary fill:#f8fafc,stroke:#64748b,color:#0f172a,stroke-dasharray:4 3
```

### tasks

```mermaid
flowchart LR
    n0["Event Backbone · current"]:::boundary
    n1["Request Lifecycle · current"]:::boundary
    n2["Resilience Model · current"]:::boundary
    n3["Security Architecture · current"]:::boundary
    n4["System Context · current"]:::boundary
    n5["Tenant Isolation · current"]:::boundary
    n6["Customer Experience delivery plan · current"]:::boundary
    n7["Data Migration delivery plan · current"]:::boundary
    n8["Adr 001: Modular Service Boundaries · accepted"]:::boundary
    n9["Adr 004: Tenant Key Partitioning · accepted"]:::boundary
    n10["Adr 007: Schema Registry Compatibility · accepted"]:::boundary
    n11["Adr 010: Central Policy Evaluation · accepted"]:::boundary
    n12["Adr 013: Progressive Delivery · accepted"]:::boundary
    n13["Adr 016: Encrypted Event Payloads · accepted"]:::boundary
    n14["Identity Security delivery plan · current"]:::boundary
    n15["Observability Release delivery plan · current"]:::boundary
    n16["Platform Foundations delivery plan · current"]:::boundary
    n17["Programme Delivery And Architecture Map · current"]:::boundary
    n18["Add migration progress centre · in-progress"]:::task
    n19["Customer Experience coordination · in-progress"]:::workstream
    n20["Add privileged access reviews · validation"]:::task
    n21["Add release health checks · in-progress"]:::task
    n22["Observability Release coordination · in-progress"]:::workstream
    n23["Approve architecture readiness · blocked"]:::task
    n24["Approve general availability · ready"]:::task
    n25["Approve production cutover data · ready"]:::task
    n26["Automate dependency updates · blocked"]:::task
    n27["Benchmark critical request paths · ready"]:::task
    n28["Build account creation flow · done"]:::task
    n29["Build change data capture pipeline · validation"]:::task
    n30["Build operational dashboards · validation"]:::task
    n31["Build shared authentication middleware · ready"]:::task
    n32["Complete guided onboarding trials · blocked"]:::task
    n33["Complete release rehearsal · blocked"]:::task
    n34["Complete threat model review · blocked"]:::task
    n35["Create cross-service trace model · done"]:::task
    n36["Create reconciliation reports · in-progress"]:::task
    n37["Data Migration coordination · in-progress"]:::workstream
    n38["Define canonical customer schema · done"]:::task
    n39["Define service level objectives · done"]:::task
    n40["Define service ownership · done"]:::task
    n41["Design recoverable form states · ready"]:::task
    n42["Enforce workload identity · in-progress"]:::task
    n43["Identity Security coordination · in-progress"]:::workstream
    n44["Establish repository boundaries · done"]:::task
    n45["Exercise rollback automation · ready"]:::task
    n46["Exercise tenant isolation · in-progress"]:::task
    n47["Harden session management · ready"]:::task
    n48["Implement organisation switching · validation"]:::task
    n49["Implement token rotation · done"]:::task
    n50["Instrument authentication failures · proposed"]:::task
    n51["Introduce feature flagging · proposed"]:::task
    n52["Inventory legacy data sources · done"]:::task
    n53["Map onboarding journey · done"]:::task
    n54["Meet accessibility acceptance · proposed"]:::task
    n55["Migrate reference data · ready"]:::task
    n56["Model tenant isolation · done"]:::task
    n57["Prototype the event backbone · validation"]:::task
    n58["Provision development environments · validation"]:::task
    n59["Publish customer experience readiness · ready"]:::task
    n60["Publish platform readiness evidence · ready"]:::task
    n61["Rehearse regional recovery · proposed"]:::task
    n62["Resolve migration exceptions · blocked"]:::task
    n63["Run customer migration rehearsal · proposed"]:::task
    n64["Run failure injection scenarios · proposed"]:::task
    n65["Standardise configuration loading · in-progress"]:::task
    n66["Platform Foundations coordination · in-progress"]:::workstream
    n67["Validate architecture decision coverage · done"]:::task
    n68["Validate security launch controls · ready"]:::task
    n0 -->|links| n10
    n1 -->|links| n11
    n2 -->|links| n13
    n4 -->|links| n8
    n6 -->|links| n53
    n6 -->|links| n28
    n6 -->|links| n48
    n6 -->|links| n18
    n6 -->|links| n41
    n6 -->|links| n54
    n6 -->|links| n32
    n6 -->|links| n59
    n7 -->|links| n52
    n7 -->|links| n38
    n7 -->|links| n29
    n7 -->|links| n36
    n7 -->|links| n55
    n7 -->|links| n63
    n7 -->|links| n62
    n7 -->|links| n25
    n8 -->|links| n4
    n10 -->|links| n0
    n12 -->|links| n4
    n14 -->|links| n56
    n14 -->|links| n49
    n14 -->|links| n20
    n14 -->|links| n42
    n14 -->|links| n47
    n14 -->|links| n50
    n14 -->|links| n34
    n14 -->|links| n68
    n15 -->|links| n39
    n15 -->|links| n35
    n15 -->|links| n30
    n15 -->|links| n21
    n15 -->|links| n45
    n15 -->|links| n64
    n15 -->|links| n33
    n15 -->|links| n24
    n16 -->|links| n44
    n16 -->|links| n40
    n16 -->|links| n58
    n16 -->|links| n65
    n16 -->|links| n31
    n16 -->|links| n51
    n16 -->|links| n26
    n16 -->|links| n60
    n17 -->|links| n4
    n17 -->|links| n8
    n17 -->|links| n16
    n17 -->|links| n44
    n17 -->|links| n67
    n18 -->|links| n48
    n18 -->|links| n53
    n18 -->|links| n6
    n19 -->|links| n28
    n19 -->|links| n48
    n19 -->|links| n41
    n19 -->|links| n54
    n19 -->|links| n32
    n19 -->|workstream| n18
    n20 -->|links| n49
    n20 -->|links| n14
    n21 -->|links| n30
    n21 -->|links| n39
    n21 -->|links| n15
    n22 -->|links| n35
    n22 -->|links| n30
    n22 -->|links| n45
    n22 -->|links| n64
    n22 -->|links| n33
    n22 -->|workstream| n21
    n23 -->|links| n61
    n23 -->|links| n3
    n23 -->|links| n13
    n24 -->|links| n33
    n24 -->|links| n45
    n24 -->|links| n15
    n25 -->|links| n62
    n25 -->|links| n55
    n25 -->|links| n7
    n26 -->|links| n51
    n26 -->|links| n65
    n26 -->|links| n16
    n27 -->|links| n46
    n27 -->|links| n0
    n27 -->|links| n11
    n28 -->|links| n53
    n28 -->|links| n6
    n29 -->|links| n38
    n29 -->|links| n7
    n30 -->|links| n35
    n30 -->|links| n15
    n31 -->|links| n65
    n31 -->|links| n40
    n31 -->|links| n16
    n32 -->|links| n54
    n32 -->|links| n18
    n32 -->|links| n6
    n33 -->|links| n64
    n33 -->|links| n21
    n33 -->|links| n15
    n34 -->|links| n50
    n34 -->|links| n42
    n34 -->|links| n14
    n35 -->|links| n39
    n35 -->|links| n15
    n36 -->|links| n29
    n36 -->|links| n52
    n36 -->|links| n7
    n37 -->|links| n38
    n37 -->|links| n29
    n37 -->|links| n55
    n37 -->|links| n63
    n37 -->|links| n62
    n37 -->|workstream| n36
    n38 -->|links| n52
    n38 -->|links| n7
    n39 -->|links| n59
    n39 -->|links| n15
    n40 -->|links| n44
    n40 -->|links| n16
    n41 -->|links| n18
    n41 -->|links| n28
    n41 -->|links| n6
    n42 -->|links| n20
    n42 -->|links| n56
    n42 -->|links| n14
    n43 -->|links| n49
    n43 -->|links| n20
    n43 -->|links| n47
    n43 -->|links| n50
    n43 -->|links| n34
    n43 -->|workstream| n42
    n44 -->|links| n16
    n45 -->|links| n21
    n45 -->|links| n35
    n45 -->|links| n15
    n46 -->|links| n57
    n46 -->|links| n5
    n46 -->|links| n10
    n47 -->|links| n42
    n47 -->|links| n49
    n47 -->|links| n14
    n48 -->|links| n28
    n48 -->|links| n6
    n49 -->|links| n56
    n49 -->|links| n14
    n50 -->|links| n47
    n50 -->|links| n20
    n50 -->|links| n14
    n51 -->|links| n31
    n51 -->|links| n58
    n51 -->|links| n16
    n52 -->|links| n68
    n52 -->|links| n7
    n53 -->|links| n25
    n53 -->|links| n6
    n54 -->|links| n41
    n54 -->|links| n48
    n54 -->|links| n6
    n55 -->|links| n36
    n55 -->|links| n38
    n55 -->|links| n7
    n56 -->|links| n60
    n56 -->|links| n14
    n57 -->|links| n67
    n57 -->|links| n1
    n57 -->|links| n9
    n58 -->|links| n40
    n58 -->|links| n16
    n59 -->|links| n32
    n59 -->|links| n41
    n59 -->|links| n6
    n60 -->|links| n26
    n60 -->|links| n31
    n60 -->|links| n16
    n61 -->|links| n27
    n61 -->|links| n2
    n61 -->|links| n12
    n62 -->|links| n63
    n62 -->|links| n36
    n62 -->|links| n7
    n63 -->|links| n55
    n63 -->|links| n29
    n63 -->|links| n7
    n64 -->|links| n45
    n64 -->|links| n30
    n64 -->|links| n15
    n65 -->|links| n58
    n65 -->|links| n44
    n65 -->|links| n16
    n66 -->|links| n40
    n66 -->|links| n58
    n66 -->|links| n31
    n66 -->|links| n51
    n66 -->|links| n26
    n66 -->|workstream| n65
    n67 -->|links| n4
    n67 -->|links| n8
    n68 -->|links| n34
    n68 -->|links| n47
    n68 -->|links| n14
    classDef task fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef workstream fill:#ede9fe,stroke:#7c3aed,color:#2e1065
    classDef tracker fill:#ffedd5,stroke:#ea580c,color:#431407
    classDef knowledge fill:#dcfce7,stroke:#16a34a,color:#052e16
    classDef boundary fill:#f8fafc,stroke:#64748b,color:#0f172a,stroke-dasharray:4 3
```

## Key concept neighbourhoods

### Platform Foundations delivery plan

```mermaid
flowchart LR
    n0["Platform Foundations delivery plan · current"]:::knowledge
    n1["Programme Delivery And Architecture Map · current"]:::boundary
    n2["Combined delivery and architecture workspace"]:::boundary
    n3["Automate dependency updates · blocked"]:::boundary
    n4["Build shared authentication middleware · ready"]:::boundary
    n5["Define service ownership · done"]:::boundary
    n6["Establish repository boundaries · done"]:::boundary
    n7["Introduce feature flagging · proposed"]:::boundary
    n8["Provision development environments · validation"]:::boundary
    n9["Publish platform readiness evidence · ready"]:::boundary
    n10["Standardise configuration loading · in-progress"]:::boundary
    n0 -->|links| n6
    n0 -->|links| n5
    n0 -->|links| n8
    n0 -->|links| n10
    n0 -->|links| n4
    n0 -->|links| n7
    n0 -->|links| n3
    n0 -->|links| n9
    n1 -->|links| n0
    n1 -->|links| n6
    n2 -->|links| n1
    n2 -->|links| n0
    n3 -->|links| n7
    n3 -->|links| n10
    n3 -->|links| n0
    n4 -->|links| n10
    n4 -->|links| n5
    n4 -->|links| n0
    n5 -->|links| n6
    n5 -->|links| n0
    n6 -->|links| n0
    n7 -->|links| n4
    n7 -->|links| n8
    n7 -->|links| n0
    n8 -->|links| n5
    n8 -->|links| n0
    n9 -->|links| n3
    n9 -->|links| n4
    n9 -->|links| n0
    n10 -->|links| n8
    n10 -->|links| n6
    n10 -->|links| n0
    classDef task fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef workstream fill:#ede9fe,stroke:#7c3aed,color:#2e1065
    classDef tracker fill:#ffedd5,stroke:#ea580c,color:#431407
    classDef knowledge fill:#dcfce7,stroke:#16a34a,color:#052e16
    classDef boundary fill:#f8fafc,stroke:#64748b,color:#0f172a,stroke-dasharray:4 3
```

### Customer Experience delivery plan

```mermaid
flowchart LR
    n0["Customer Experience delivery plan · current"]:::knowledge
    n1["Add migration progress centre · in-progress"]:::boundary
    n2["Build account creation flow · done"]:::boundary
    n3["Complete guided onboarding trials · blocked"]:::boundary
    n4["Design recoverable form states · ready"]:::boundary
    n5["Implement organisation switching · validation"]:::boundary
    n6["Map onboarding journey · done"]:::boundary
    n7["Meet accessibility acceptance · proposed"]:::boundary
    n8["Publish customer experience readiness · ready"]:::boundary
    n0 -->|links| n6
    n0 -->|links| n2
    n0 -->|links| n5
    n0 -->|links| n1
    n0 -->|links| n4
    n0 -->|links| n7
    n0 -->|links| n3
    n0 -->|links| n8
    n1 -->|links| n5
    n1 -->|links| n6
    n1 -->|links| n0
    n2 -->|links| n6
    n2 -->|links| n0
    n3 -->|links| n7
    n3 -->|links| n1
    n3 -->|links| n0
    n4 -->|links| n1
    n4 -->|links| n2
    n4 -->|links| n0
    n5 -->|links| n2
    n5 -->|links| n0
    n6 -->|links| n0
    n7 -->|links| n4
    n7 -->|links| n5
    n7 -->|links| n0
    n8 -->|links| n3
    n8 -->|links| n4
    n8 -->|links| n0
    classDef task fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef workstream fill:#ede9fe,stroke:#7c3aed,color:#2e1065
    classDef tracker fill:#ffedd5,stroke:#ea580c,color:#431407
    classDef knowledge fill:#dcfce7,stroke:#16a34a,color:#052e16
    classDef boundary fill:#f8fafc,stroke:#64748b,color:#0f172a,stroke-dasharray:4 3
```

### Data Migration delivery plan

```mermaid
flowchart LR
    n0["Data Migration delivery plan · current"]:::knowledge
    n1["Approve production cutover data · ready"]:::boundary
    n2["Build change data capture pipeline · validation"]:::boundary
    n3["Create reconciliation reports · in-progress"]:::boundary
    n4["Define canonical customer schema · done"]:::boundary
    n5["Inventory legacy data sources · done"]:::boundary
    n6["Migrate reference data · ready"]:::boundary
    n7["Resolve migration exceptions · blocked"]:::boundary
    n8["Run customer migration rehearsal · proposed"]:::boundary
    n0 -->|links| n5
    n0 -->|links| n4
    n0 -->|links| n2
    n0 -->|links| n3
    n0 -->|links| n6
    n0 -->|links| n8
    n0 -->|links| n7
    n0 -->|links| n1
    n1 -->|links| n7
    n1 -->|links| n6
    n1 -->|links| n0
    n2 -->|links| n4
    n2 -->|links| n0
    n3 -->|links| n2
    n3 -->|links| n5
    n3 -->|links| n0
    n4 -->|links| n5
    n4 -->|links| n0
    n5 -->|links| n0
    n6 -->|links| n3
    n6 -->|links| n4
    n6 -->|links| n0
    n7 -->|links| n8
    n7 -->|links| n3
    n7 -->|links| n0
    n8 -->|links| n6
    n8 -->|links| n2
    n8 -->|links| n0
    classDef task fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef workstream fill:#ede9fe,stroke:#7c3aed,color:#2e1065
    classDef tracker fill:#ffedd5,stroke:#ea580c,color:#431407
    classDef knowledge fill:#dcfce7,stroke:#16a34a,color:#052e16
    classDef boundary fill:#f8fafc,stroke:#64748b,color:#0f172a,stroke-dasharray:4 3
```

### Identity Security delivery plan

```mermaid
flowchart LR
    n0["Identity Security delivery plan · current"]:::knowledge
    n1["Add privileged access reviews · validation"]:::boundary
    n2["Complete threat model review · blocked"]:::boundary
    n3["Enforce workload identity · in-progress"]:::boundary
    n4["Harden session management · ready"]:::boundary
    n5["Implement token rotation · done"]:::boundary
    n6["Instrument authentication failures · proposed"]:::boundary
    n7["Model tenant isolation · done"]:::boundary
    n8["Validate security launch controls · ready"]:::boundary
    n0 -->|links| n7
    n0 -->|links| n5
    n0 -->|links| n1
    n0 -->|links| n3
    n0 -->|links| n4
    n0 -->|links| n6
    n0 -->|links| n2
    n0 -->|links| n8
    n1 -->|links| n5
    n1 -->|links| n0
    n2 -->|links| n6
    n2 -->|links| n3
    n2 -->|links| n0
    n3 -->|links| n1
    n3 -->|links| n7
    n3 -->|links| n0
    n4 -->|links| n3
    n4 -->|links| n5
    n4 -->|links| n0
    n5 -->|links| n7
    n5 -->|links| n0
    n6 -->|links| n4
    n6 -->|links| n1
    n6 -->|links| n0
    n7 -->|links| n0
    n8 -->|links| n2
    n8 -->|links| n4
    n8 -->|links| n0
    classDef task fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef workstream fill:#ede9fe,stroke:#7c3aed,color:#2e1065
    classDef tracker fill:#ffedd5,stroke:#ea580c,color:#431407
    classDef knowledge fill:#dcfce7,stroke:#16a34a,color:#052e16
    classDef boundary fill:#f8fafc,stroke:#64748b,color:#0f172a,stroke-dasharray:4 3
```

### Observability Release delivery plan

```mermaid
flowchart LR
    n0["Observability Release delivery plan · current"]:::knowledge
    n1["Add release health checks · in-progress"]:::boundary
    n2["Approve general availability · ready"]:::boundary
    n3["Build operational dashboards · validation"]:::boundary
    n4["Complete release rehearsal · blocked"]:::boundary
    n5["Create cross-service trace model · done"]:::boundary
    n6["Define service level objectives · done"]:::boundary
    n7["Exercise rollback automation · ready"]:::boundary
    n8["Run failure injection scenarios · proposed"]:::boundary
    n0 -->|links| n6
    n0 -->|links| n5
    n0 -->|links| n3
    n0 -->|links| n1
    n0 -->|links| n7
    n0 -->|links| n8
    n0 -->|links| n4
    n0 -->|links| n2
    n1 -->|links| n3
    n1 -->|links| n6
    n1 -->|links| n0
    n2 -->|links| n4
    n2 -->|links| n7
    n2 -->|links| n0
    n3 -->|links| n5
    n3 -->|links| n0
    n4 -->|links| n8
    n4 -->|links| n1
    n4 -->|links| n0
    n5 -->|links| n6
    n5 -->|links| n0
    n6 -->|links| n0
    n7 -->|links| n1
    n7 -->|links| n5
    n7 -->|links| n0
    n8 -->|links| n7
    n8 -->|links| n3
    n8 -->|links| n0
    classDef task fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef workstream fill:#ede9fe,stroke:#7c3aed,color:#2e1065
    classDef tracker fill:#ffedd5,stroke:#ea580c,color:#431407
    classDef knowledge fill:#dcfce7,stroke:#16a34a,color:#052e16
    classDef boundary fill:#f8fafc,stroke:#64748b,color:#0f172a,stroke-dasharray:4 3
```

### System Context

```mermaid
flowchart LR
    n0["System Context · current"]:::knowledge
    n1["Adr 001: Modular Service Boundaries · accepted"]:::boundary
    n2["Adr 008: Zero Downtime Database Change · accepted"]:::boundary
    n3["Adr 013: Progressive Delivery · accepted"]:::boundary
    n4["Programme Delivery And Architecture Map · current"]:::boundary
    n5["Audit Service · current"]:::boundary
    n6["Identity Service · current"]:::boundary
    n7["Migration Service · current"]:::boundary
    n8["Combined delivery and architecture workspace"]:::boundary
    n9["Validate architecture decision coverage · done"]:::boundary
    n0 -->|links| n1
    n0 -->|links| n2
    n0 -->|links| n6
    n0 -->|links| n7
    n1 -->|links| n0
    n3 -->|links| n0
    n4 -->|links| n0
    n4 -->|links| n1
    n4 -->|links| n9
    n5 -->|links| n0
    n6 -->|links| n0
    n8 -->|links| n4
    n8 -->|links| n0
    n9 -->|links| n0
    n9 -->|links| n1
    classDef task fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef workstream fill:#ede9fe,stroke:#7c3aed,color:#2e1065
    classDef tracker fill:#ffedd5,stroke:#ea580c,color:#431407
    classDef knowledge fill:#dcfce7,stroke:#16a34a,color:#052e16
    classDef boundary fill:#f8fafc,stroke:#64748b,color:#0f172a,stroke-dasharray:4 3
```

## Legend

- Blue: task
- Purple: workstream
- Orange: tracker profile
- Green: durable knowledge
- Dashed neutral nodes: neighbouring context repeated from another area or key-concept view
- Time references: edges to addressable `Task.time[]` fragments
- Arrows: structured relationships or repository-local Markdown links
