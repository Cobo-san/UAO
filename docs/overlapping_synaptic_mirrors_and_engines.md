# 🪞⚡ **QENTA-PRIME Overlapping Mirrors, Synaptic Kernels & Engines Matrix**

This document details the redundant overlapping mirrors across Nodes, MCP Gateways, Synaptic Kernels, and Multimodal Engines.

| Mirror ID | Category | Description & Redundancy Topology | Target Binding | Status |
| :--- | :--- | :--- | :--- | :---: |
| `mirror_node_nvme_dual` | **NODE_MIRROR** | Primary NVMe C: (Sabrent 7,000 MB/s) <-> Secondary NVMe D: (Samsung 7,000 MB/s) | `Drive C: / Drive D:` | `OVERLAPPING_REDUNDANT_ACTIVE` |
| `mirror_node_gcp_regional` | **NODE_MIRROR** | GCP us-east1 <-> us-central1 <-> us-west1 Regional Free-Tier Mesh | `GCP Cloud Regions` | `OVERLAPPING_REDUNDANT_ACTIVE` |
| `mirror_mcp_gemini_slack` | **MCP_MIRROR** | Gemini HTTPS MCP (Port 8444) <-> Slack Remote HTTPS MCP (Port 8445) | `Port 8444 / 8445` | `OVERLAPPING_REDUNDANT_ACTIVE` |
| `mirror_mcp_anaconda_kernel` | **MCP_MIRROR** | Anaconda Server AI MCP (Port 8099) <-> Synaptic Kernel Router (Port 8080) | `Port 8099 / 8080` | `OVERLAPPING_REDUNDANT_ACTIVE` |
| `mirror_kernel_avx2_simd` | **SYNAPTIC_KERNEL** | AVX2 SIMD INT4 Accelerator Engine (CYLINDER_18 - < 0.95 ms GEMV) | `Intel i9-14900K` | `OVERLAPPING_REDUNDANT_ACTIVE` |
| `mirror_kernel_freebsd_metal` | **SYNAPTIC_KERNEL** | FreeBSD 14.1 (kern.securelevel=2) <-> FreeBSD 15 (security.bsd.hardened=YES) | `Drive E: / Drive H:` | `OVERLAPPING_REDUNDANT_ACTIVE` |
| `mirror_engine_locutus_weights` | **ENGINE_MIRROR** | Locutus 12-Agent Neural Gateway (locutus_neural_weights.sqlite) | `Port 8081 / DB` | `OVERLAPPING_REDUNDANT_ACTIVE` |
| `mirror_engine_exo_p2p_mesh` | **ENGINE_MIRROR** | Exo P2P Distributed Mesh Cluster Engine (Port 50050) | `Port 50050` | `OVERLAPPING_REDUNDANT_ACTIVE` |
| `mirror_engine_voice_vision` | **ENGINE_MIRROR** | Whisper STT (8094) + Piper TTS (8095) + LLaVA Vision OCR (8096) | `Ports 8094-8096` | `OVERLAPPING_REDUNDANT_ACTIVE` |
