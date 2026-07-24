#!/usr/bin/env python3
"""
Cluster Agent Organization Chart Generator
Generates a visual Mermaid diagram and architecture chart detailing all Executive Directors,
Domain Managers, Cluster Agent Nodes, Mirrors, Storage Drives, Anaconda Stack, and Multi-Cloud integrations.
"""

import os
import platform

def generate_org_chart():
    markdown_content = """# 🌐 UAO Cluster Agent Organization Chart & Multi-Cloud Architecture

**Repository Target:** [https://github.com/Cobo-san/UAO](https://github.com/Cobo-san/UAO)  
**GCP Project:** `anaconda-google-project-sounddharma` (`sounddharma@gmail.com`)  
**Financial Policy:** `$0.00 / Month` (100% Free Tier Guaranteed)  
**Execution Policy:** 100% System DDR5 RAM (`tmpfs` / `/dev/shm`)  
**Hardware Protection:** 100% Read-Only (`:ro` Mount / `chmod 444`)

---

## 📊 1. Visual Cluster Agent & Multi-Cloud Hierarchy (Mermaid Diagram)

```mermaid
graph TD
    %% Executive Level
    subgraph EXECUTIVE_GOVERNANCE ["👑 Executive Director Level"]
        DIR["Executive Synaptic Director<br/>(Llama-3.3-70B | Port 8090)"]
        SEC["Cybersecurity & Zero-Trust Director<br/>(DeepSeek-R1-70B | Port 8092)"]
    end

    %% Domain Managers Level
    subgraph DOMAIN_MANAGERS ["🛡️ Domain Manager Level"]
        M1["Voice & Dialogue Manager<br/>(Whisper + Piper | Port 8094)"]
        M2["Vision & Terminal Automation Manager<br/>(LLaVA-v1.6 | Port 8096)"]
        M3["Code, SDK & ADK Manager<br/>(Qwen-2.5-Coder-32B | Port 8091)"]
        M4["Creative Media & UI Manager<br/>(FLUX.1 + MusicGen | Port 8097)"]
    end

    %% Cluster Agents & Mirrors
    subgraph CLUSTER_MIRRORS ["⚡ Cluster Agents & Mirror Managers"]
        LEADER["Master Assembly Orchestrator<br/>(Port 8081)"]
        MIR1["Mirror 1 Skill Manager<br/>(47 Skills | Port 8082)"]
        MIR2["Mirror 2 Vector Manager<br/>(62 Vector Nodes | Port 8083)"]
        MIR3["Mirror 3 Env Manager<br/>(741 Extensions | Port 8084)"]
        RAG["Agent RAG Vector Search<br/>(Cosine Engine | Port 8085)"]
    end

    %% Physical Storage Housing
    subgraph PHYSICAL_STORAGE ["💾 Tri-Drive Read-Only Model Housing (372 GB)"]
        DRIVE_C["C: Primary NVMe (7,000 MB/s)<br/>Llama 70B, Qwen 32B, DeepSeek R1, Codestral 22B"]
        DRIVE_D["D: Secondary NVMe (3,500 MB/s)<br/>Llama 70B, Qwen 32B, DeepSeek R1, Codestral 22B"]
        DRIVE_E["E: Tertiary Bus (1,400 MB/s)<br/>Llama 70B, Qwen 32B, DeepSeek R1, Codestral 22B"]
    end

    %% Anaconda AI Platform Stack
    subgraph ANACONDA_STACK ["🐍 Anaconda AI Platform & Environmental Stack"]
        STUDIO["Anaconda AI Studio<br/>(http://localhost:8090/v1)"]
        FW["7 Conda Frameworks<br/>(PyTorch, TensorFlow, Scikit, LangChain, LlamaIndex, Transformers, OpenCV)"]
        CATALOG["18 LLM Catalog Entries"]
    end

    %% Multi-Cloud & OS Integrations
    subgraph MULTI_CLOUD ["☁️ Multi-Cloud & Cross-OS Integrations ($0.00/mo)"]
        GCP_WIN["GCP us-east1<br/>Windows Core Host"]
        GCP_ALMA["GCP us-central1<br/>AlmaLinux-10 Node"]
        GCP_UBU["GCP us-west1<br/>Ubuntu 24.04 Node"]
        BSD["FreeBSD Cloud Desktop<br/>(RDP Port 3389)"]
        WSL["WSL2 Linux Kernel<br/>(Ollama Port 11434)"]
    end

    %% Relationships
    DIR --> M1
    DIR --> M2
    DIR --> M3
    DIR --> M4
    SEC --> DIR
    DIR --> LEADER

    LEADER --> MIR1
    LEADER --> MIR2
    LEADER --> MIR3
    LEADER --> RAG

    M1 --> DRIVE_C
    M2 --> DRIVE_D
    M3 --> DRIVE_E

    STUDIO --> CATALOG
    STUDIO --> FW

    DIR --> GCP_WIN
    LEADER --> GCP_ALMA
    LEADER --> GCP_UBU
    LEADER --> BSD
    LEADER --> WSL
```

---

## 🏢 2. Executive & Domain Manager Node Breakdown

| Node ID | Node Name | Level / Role | Engine Model | MCP Kernel Server | Network Port |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **`agent_executive_director`** | **Executive Synaptic Director** | `DIRECTOR` | `Llama-3.3-70B-Instruct` | `kernel_executive_director_mcp` | **Port 8090** |
| **`agent_cybersecurity_director`** | **Cybersecurity & Zero-Trust Director** | `DIRECTOR_SECURITY` | `DeepSeek-R1-70B` | `kernel_cybersecurity_governance_mcp` | **Port 8092** |
| **`agent_voice_manager`** | **Voice & Dialogue Manager** | `MANAGER` | `Whisper.cpp` + `Piper TTS` | `kernel_voice_dialogue_mcp` | **Port 8094** |
| **`agent_vision_terminal_manager`** | **Vision & Terminal Manager** | `MANAGER` | `LLaVA-v1.6` / `Qwen2-VL` | `kernel_vision_terminal_mcp` | **Port 8096** |
| **`agent_code_sdk_manager`** | **Code, SDK & ADK Manager** | `MANAGER` | `Qwen-2.5-Coder-32B` | `kernel_code_sdk_mcp` | **Port 8091** |
| **`agent_media_manager`** | **Creative Media & UI Manager** | `MANAGER` | `FLUX.1` + `MusicGen` | `kernel_media_creation_mcp` | **Port 8097** |

---

## ⚡ 3. Cluster Agents, Mirrors, & Node Metrics

* **`master_assembly_orchestrator`** (**Port 8081**): Master Cluster Leader directing all mirror nodes.
* **`skill_cluster_manager_mirror1`** (**Port 8082**): Manages **47 Custom Agent Skills** (science plugins, android-cli, etc.).
* **`vector_cluster_manager_mirror2`** (**Port 8083**): Manages **62 Vector Nodes** & SQLite vector matrices.
* **`settings_cluster_manager_mirror3`** (**Port 8084**): Manages **741 IDE Extensions**, environment tokens & settings.
* **`agent_rag`** (**Port 8085**): Cosine RAG search engine across global documentation.

---

## 🐍 4. Anaconda AI Platform & Environmental Stack

* **GCP Project Integration**: `anaconda-google-project-sounddharma` (`sounddharma@gmail.com`)
* **Anaconda AI Studio Endpoint**: `http://localhost:8090/v1` (Serves local GGUF models via OpenAI-compatible `llama.cpp` API)
* **7 Registered Frameworks**: PyTorch, TensorFlow, Scikit-learn, LangChain, LlamaIndex, Transformers, OpenCV
* **Catalog Capacity**: **18 Registered LLM Catalog Entries** across `C:`, `D:`, `E:` drives

---

## ☁️ 5. Multi-Cloud & Native OS Integrations ($0.00 / Month)

* **GCP `us-east1`**: Windows Core Host Node (100% Free Tier Eligible)
* **GCP `us-central1`**: AlmaLinux-10 Cluster Node (`e2-micro` Free Tier)
* **GCP `us-west1`**: Ubuntu 24.04 LTS Cluster Node (`e2-micro` Free Tier)
* **FreeBSD Oracle Cloud Desktop**: Native GUI desktop environment (RDP **Port 3389**)
* **WSL2 Linux Kernel**: Standalone Linux Ollama v0.32.3 daemon (**Port 11434**)
"""

    output_path = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\templates\cluster_agent_org_chart.md"
    if platform.system() != "Windows":
        output_path = "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/templates/cluster_agent_org_chart.md"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"[+] Generated Cluster Agent Organization Chart Blueprint: {output_path}")

if __name__ == "__main__":
    generate_org_chart()
