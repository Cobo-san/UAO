# 🌐 Multi-Model Orchestration & Dynamic Routing Blueprint

**Repository:** [https://github.com/Cobo-san/UAO](https://github.com/Cobo-san/UAO)  
**Orchestration Policy:** Automated Intent-Based Prompt Routing across Local LLM Kernels

---

## 🧭 Multi-Model Routing Architecture

The **UAO System** uses an automated **Dynamic Intent Router** ([dynamic_multi_model_router.py](file:///C:/Users/Monica%20Fugazi/.antigravity-ide/living_repository/bin/dynamic_multi_model_router.py)) that inspects incoming user queries and subagent requests to route them to the specialized model best equipped to handle them.

```
                                  ┌────────────────────────────────────────────────┐
                                  │      DYNAMIC INTENT ROUTER ENGINE              │
                                  │    (dynamic_multi_model_router.py)             │
                                  └───────────────────────┬────────────────────────┘
                                                          │
         ┌───────────────────────────┬────────────────────┴────────────────┬───────────────────────────┐
         │                           │                                     │                           │
         ▼                           ▼                                     ▼                           ▼
┌─────────────────┐         ┌──────────────────┐                  ┌──────────────────┐        ┌─────────────────┐
│ Llama-3.3-70B   │         │ Qwen-2.5-Coder   │                  │ DeepSeek-R1-70B  │        │ Codestral-22B   │
│ (Port 8090)     │         │ (Port 8091)      │                  │ (Port 8092)      │        │ (Port 8093)     │
└────────┬────────┘         └────────┬─────────┘                  └────────┬─────────┘        └────────┬────────┘
         │                           │                                     │                           │
  Master Planning &           Python SDK, Android ADK,              Protocol Debugging,        Fast Subagent Tasks,
  System Architecture         Networking & gRPC Code                Race Conditions & Math     Unit Tests & Linting
```

---

## 🎯 Model Domain Matrix

| Model | Assigned Port | Primary Task Domain | Target Keywords / Intent |
| :--- | :--- | :--- | :--- |
| **Llama-3.3-70B** | `Port 8090` | **Master System Orchestration** | Architecture, System Plans, Multi-Cloud Strategy, Documentation |
| **Qwen-2.5-Coder-32B** | `Port 8091` | **SDK, ADK & Network Code** | Python SDK, Android ADK (Kotlin/Java/NDK), gRPC, Sockets, REST APIs |
| **DeepSeek-R1-Distill-70B** | `Port 8092` | **Deep Reasoning & Debugging**| Protocol Deadlocks, Race Conditions, Stack Trace Analysis, Math Proofs |
| **Codestral-22B** | `Port 8093` | **Fast Subagent Automation** | Unit Tests, Lint Fixes, Quick Refactoring, Instant Responses |

---

## ⚡ Technical Execution Workflow

1. **Prompt Ingestion**: Incoming prompt enters the UAO Master Orchestrator.
2. **Intent Classification**: [dynamic_multi_model_router.py](file:///C:/Users/Monica%20Fugazi/.antigravity-ide/living_repository/bin/dynamic_multi_model_router.py) scans regex domain patterns (`sdk`, `android`, `debug`, `architecture`).
3. **Synaptic MCP Dispatch**: The query is dispatched to the corresponding Synaptic MCP Kernel (`kernel_native_llama70b`, `kernel_qwen_coder32b`, `kernel_deepseek_r1`).
4. **Read-Only NVMe Model Execution**: The selected model generates the response using the read-only GGUF weights on `D:` or `C:` NVMe.
