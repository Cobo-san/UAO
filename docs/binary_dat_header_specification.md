# 📟 **32-Byte Binary `.dat` Header Specification**

This document specifies the binary `.dat` IPC headers used across QENTA-PRIME UAO for zero-token binary communications.

---

## 🔬 **Binary Structure Layout (32 Bytes)**

```c
struct AntigravityBinaryHeader {
    uint32_t magic;         // 0x41494756 ("AIGV")
    uint32_t version;       // Protocol Version (0x00000002)
    uint32_t node_id;       // Target Port / Node ID (e.g. 8091, 50050)
    uint32_t flags;         // Operational Flags (0x00000001 = ARMED)
    uint8_t  reserved[16];  // 16-Byte Reserved Telemetry Padding
};
```

---

## 📂 **Active `.dat` Binary Header Files**

- 📄 [kimi_k27_code_binary_header.dat](file:///C:/Users/Monica%20Fugazi/.antigravity-ide/living_repository/bin/kimi_k27_code_binary_header.dat) — Kimi K2.7-Code IPC Header (Node 8091)
- 📄 [exo_mesh_p2p_cluster_header.dat](file:///C:/Users/Monica%20Fugazi/.antigravity-ide/living_repository/bin/exo_mesh_p2p_cluster_header.dat) — Exo P2P Mesh Cluster Header (Node 50050)
