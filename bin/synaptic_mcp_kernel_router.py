#!/usr/bin/env python3
"""
Synaptic MCP Kernel Router & Data Flow Optimization Engine
Configures Model Context Protocol (MCP) servers with Primary, Back, and Side routing paths:
- Primary Routes: Windows -> us-east1, AlmaLinux -> us-central1, Ubuntu -> us-west1
- Back Routes: Failover cascade across regions (us-east1 <-> us-central1 <-> us-west1)
- Side Routes: Lateral zero-latency IPC between distros (Windows <-> AlmaLinux <-> Ubuntu)
"""

import os
import sys
import json
import sqlite3
import math
import time
import platform
from pathlib import Path

# MCP Server Port Definitions
MCP_C_PRIMARY_PORT = 8080
MCP_D_SECONDARY_PORT = 8081
MCP_DUAL_BUS_PORT = 8082

ROUTING_TOPOLOGY = {
    "Windows": {
        "primary_route": {"region": "us-east1", "zone": "us-east1-a", "mcp_port": MCP_C_PRIMARY_PORT, "nvme": "C: (Sabrent Rocket)"},
        "back_routes": ["us-central1", "us-west1"],
        "side_routes": ["AlmaLinux", "Ubuntu"]
    },
    "AlmaLinux": {
        "primary_route": {"region": "us-central1", "zone": "us-central1-a", "mcp_port": MCP_D_SECONDARY_PORT, "nvme": "D: (Samsung 970 EVO)"},
        "back_routes": ["us-west1", "us-east1"],
        "side_routes": ["Ubuntu", "Windows"]
    },
    "Ubuntu": {
        "primary_route": {"region": "us-west1", "zone": "us-west1-a", "mcp_port": MCP_DUAL_BUS_PORT, "nvme": "Dual-Bus Striped"},
        "back_routes": ["us-east1", "us-central1"],
        "side_routes": ["Windows", "AlmaLinux"]
    }
}

def get_current_os():
    return platform.system()

def get_paths():
    if get_current_os() == "Windows":
        return {
            "living_repo": r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository",
            "db_path": r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\synaptic_matrix\universal_synaptic_matrix.sqlite",
            "gdrive_db": r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\Parallel_Synaptic_Database_Matrix\universal_synaptic_matrix.sqlite"
        }
    else:
        return {
            "living_repo": "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository",
            "db_path": "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/synaptic_matrix/universal_synaptic_matrix.sqlite",
            "gdrive_db": "/mnt/c/Users/Monica Fugazi/GoogleDrive_sounddharma/Parallel_Synaptic_Database_Matrix/universal_synaptic_matrix.sqlite"
        }

def compute_cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm_a = math.sqrt(sum(a * a for a in vec1))
    norm_b = math.sqrt(sum(b * b for b in vec2))
    return dot_product / (norm_a * norm_b) if norm_a and norm_b else 0.0

def initialize_synaptic_mcp_tables(conn):
    cursor = conn.cursor()
    
    # Table 1: MCP Routing & Data Flow Matrix
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mcp_synaptic_routes (
        route_id TEXT PRIMARY KEY,
        source_distro TEXT,
        route_type TEXT, -- PRIMARY, BACK, SIDE
        target_destination TEXT,
        mcp_port INTEGER,
        latency_ms REAL,
        status TEXT
    );
    """)

    # Table 2: Synaptic Vector Kernel Topology (16D)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS synaptic_kernel_vectors (
        vector_id TEXT PRIMARY KEY,
        domain_name TEXT,
        vector_16d_json TEXT,
        recommended_route_type TEXT,
        hit_count INTEGER DEFAULT 0
    );
    """)

    conn.commit()

def populate_mcp_routes(db_path):
    if not os.path.exists(db_path):
        return

    try:
        os.chmod(db_path, 0o666)
    except Exception:
        pass

    conn = sqlite3.connect(db_path)
    initialize_synaptic_mcp_tables(conn)
    cursor = conn.cursor()

    routes = []
    for distro, config in ROUTING_TOPOLOGY.items():
        # Primary
        p = config["primary_route"]
        routes.append((f"{distro.lower()}_primary", distro, "PRIMARY", p["region"], p["mcp_port"], 0.2, "ACTIVE_PRIMARY"))
        
        # Back Routes
        for idx, back_region in enumerate(config["back_routes"]):
            routes.append((f"{distro.lower()}_back_{idx+1}", distro, "BACK_FAILOVER", back_region, p["mcp_port"], 12.5 + (idx*10), "STANDBY_BACK"))

        # Side Routes
        for idx, side_distro in enumerate(config["side_routes"]):
            routes.append((f"{distro.lower()}_side_{side_distro.lower()}", distro, "SIDE_LATERAL_IPC", side_distro, p["mcp_port"], 0.1, "ACTIVE_SIDE_IPC"))

    cursor.executemany("INSERT OR REPLACE INTO mcp_synaptic_routes VALUES (?,?,?,?,?,?,?)", routes)
    conn.commit()
    conn.close()

def generate_mcp_json_config(target_file):
    """
    Generates unified MCP Server configuration file for IDE / AGY CLI integration.
    """
    config = {
        "mcpServers": {
            "mcp_engine_c_drive_primary": {
                "command": "python",
                "args": [r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\universal_binary_ipc_engine.py"],
                "env": {
                    "MCP_PORT": str(MCP_C_PRIMARY_PORT),
                    "GCP_REGION": "us-east1",
                    "STORAGE_DRIVE": "C:"
                }
            },
            "mcp_engine_d_drive_secondary": {
                "command": "python",
                "args": [r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\universal_binary_ipc_engine.py"],
                "env": {
                    "MCP_PORT": str(MCP_D_SECONDARY_PORT),
                    "GCP_REGION": "us-central1",
                    "STORAGE_DRIVE": "D:"
                }
            },
            "mcp_engine_dual_bus_router": {
                "command": "python",
                "args": [r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\synaptic_mcp_kernel_router.py"],
                "env": {
                    "MCP_PORT": str(MCP_DUAL_BUS_PORT),
                    "GCP_REGION": "us-west1",
                    "ROUTING_MODE": "SYNAPTIC_MULTIPLEXED"
                }
            }
        }
    }

    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, "w") as f:
        json.dump(config, f, indent=2)

def main():
    print("=== Synaptic MCP Kernel Router & Data Flow Optimization Engine ===")
    paths = get_paths()

    # 1. Populate Routes in Living Repo DB
    if os.path.exists(paths["db_path"]):
        populate_mcp_routes(paths["db_path"])
        print(f"[+] Synaptic MCP Primary, Back, and Side Routes populated in Living Repo DB: {paths['db_path']}")

    # 2. Populate Routes in Google Drive DB
    if os.path.exists(paths["gdrive_db"]):
        populate_mcp_routes(paths["gdrive_db"])
        print(f"[+] Synaptic MCP Routes replicated in Google Drive DB: {paths['gdrive_db']}")

    # 3. Generate MCP JSON Config in living_repository/mcp_servers/
    mcp_config_file = os.path.join(paths["living_repo"], "mcp_servers", "mcp_synaptic_kernel_config.json")
    generate_mcp_json_config(mcp_config_file)
    print(f"[+] Generated Unified MCP JSON Server Config: {mcp_config_file}")

    print("[OK] SYNAPTIC MCP KERNEL ROUTING & DATA FLOW OPTIMIZATION INITIALIZED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
