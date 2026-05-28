# ACME Omniscient: Self-Defending Autonomous Support & Logistics Ecosystem

A production-grade, local-first AI agent architecture built using Python and Llama 3.2. This system is designed to handle specialized e-commerce operations, deterministic financial tooling, and semantic knowledge retrieval while implementing strict input/output defensive guardrails and performance failover routing.

## 🏗️ System Architecture Topology

```mermaid
graph TD
    A[📥 Raw Inbound User Request] --> B{1. Input Guardrail Node}
    
    B -->|BLOCKED| C[🚨 Security Exception: Access Denied]
    B -->|PASSED| D[🟢 2. Local RAG Context Engine]
    
    D -->|Extracts core_policy.txt| E[🧠 3. Multi-Turn Agent Core]
    
    E --> F{Dynamic Tool Router}
    F -->|Math Request| G[⚙️ calculate_restocking_fee]
    F -->|Logistics Request| H[📦 evaluate_shipping_carrier]
    
    G --> I{4. Output QA Compliance Gate}
    H --> I
    
    I -->|HALLUCINATION DETECTED| J[🚨 Quarantine / Operational Notice]
    I -->|PASS| K[📊 5. Telemetry Analytics Hub]
    
    K --> L[🖥️ Verified User Display]

    %% Styling Theme to make it look incredibly sharp
    style B fill:#1f2937,stroke:#ef4444,stroke-width:2px,color:#fff
    style I fill:#1f2937,stroke:#f59e0b,stroke-width:2px,color:#fff
    style C fill:#7f1d1d,stroke:#ef4444,color:#fff
    style J fill:#7f1d1d,stroke:#f59e0b,color:#fff
    style L fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#fff
```

## 🛠️ Technical Implementation Breakdown

* **🛡️ Asymmetric Input Perimeter (Week 8):** Implements an upstream Guardrail Firewall Node that intercept text tokens to validate context strings against malicious prompt injections, system-level bypass commands, or social engineering exploits.
* **🗄️ Contextual Semantic Memory (Weeks 1-4):** Operates a localized Retrieval-Augmented Generation (RAG) data flow that extracts true reference policy statements to anchor agent output within specified operational parameters.
* **⚙️ Tool-Augmented Agent Control (Week 7):** Integrates standard natural language processing with strict, deterministic Python calculation endpoints using structural model function calling protocols.
* **🔍 Factual Output Verification Gate (Week 8):** Features a back-door Quality Assurance auditor loop that parses raw structural output data streams against original facts to detect and quarantine hallucinations before delivery.
* **📊 Performance Telemetry Tracking (Week 8):** Measures system overhead including transaction latency, token throughput speeds, and triggers a circuit-breaking **Hybrid Failover Proxy Router** if local hardware limits breach target SLAs.

## 🚀 Local Installation & Execution

1. Ensure a local instance of Ollama is running with Llama 3.2 available:
   ```bash
   ollama run llama3.2