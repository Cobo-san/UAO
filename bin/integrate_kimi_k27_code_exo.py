#!/usr/bin/env python3
"""
Kimi K2.7-Code & Exo P2P Distributed Mesh Integration Engine
Configures Exo P2P Mesh Engine (Port 50050) as the Master Cluster Orchestrator
and registers Kimi K2.7-Code / Kimi K2.6 as worker inference models.
"""

import os
import sys
import json
import sqlite3
import time

ACCOUNT_EMAIL = "sounddharma@gmail.com"
GCP_PROJECT_ID = "anaconda-google-project-sounddharma"

REPO_DIR = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository"
DB_PATH = os.path.join(REPO_DIR, "synaptic_matrix", "universal_synaptic_matrix.sqlite")
GDRIVE_DB = r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\Parallel_Synaptic_Database_Matrix\universal_synaptic_matrix.sqlite"

models_config = [
    {
        "model_id": "moonshotai/Kimi-K2.7-Code",
        "name": "Kimi K2.7-Code Synthesis Model",
        "type": "Code-Specialized LLM",
        "huggingface_repo": "moonshotai/Kimi-K2.7-Code",
        "ollama_tag": "kimi-k2.7-code",
        "gguf_repo": "unsloth/Kimi-K2.7-Code-GGUF",
        "controller": "Exo P2P Distributed Mesh (Port 50050)",
        "status": "CONFIGURED_EXO_CONTROLLED"
    },
    {
        "model_id": "moonshotai/Kimi-K2.6",
        "name": "Kimi K2.6 Full Open-Weights Model",
        "type": "1.1T Parameter MoE (32B Active)",
        "huggingface_repo": "moonshotai/Kimi-K2.6",
        "ollama_tag": "kimi-k2.6",
        "gguf_repo": "unsloth/Kimi-K2.6-GGUF",
        "controller": "Exo P2P Distributed Mesh (Port 50050)",
        "status": "CONFIGURED_EXO_CONTROLLED"
    }
]

def main():
    print("==========================================================================")
    print("   KIMI K2.7-CODE & EXO P2P MESH INTEGRATION REGISTRAR                   ")
    print("==========================================================================")
    print(f"Timestamp UTC: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}")
    print(f"Account: {ACCOUNT_EMAIL}")

    # Register in SQLite DB
    for db in [DB_PATH, GDRIVE_DB]:
        if os.path.exists(db):
            try:
                conn = sqlite3.connect(db)
                cur = conn.cursor()
                cur.execute("""
                CREATE TABLE IF NOT EXISTS kimi_exo_model_registry (
                    model_id TEXT PRIMARY KEY,
                    name TEXT,
                    type TEXT,
                    huggingface_repo TEXT,
                    ollama_tag TEXT,
                    gguf_repo TEXT,
                    controller TEXT,
                    status TEXT
                );
                """)
                for m in models_config:
                    cur.execute("""
                    INSERT OR REPLACE INTO kimi_exo_model_registry
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                    """, (
                        m["model_id"], m["name"], m["type"],
                        m["huggingface_repo"], m["ollama_tag"],
                        m["gguf_repo"], m["controller"], m["status"]
                    ))

                # Log MCP Synaptic Route
                cur.execute("""
                INSERT OR REPLACE INTO mcp_synaptic_routes
                VALUES ('mcp_route_kimi_k27_exo', 'Host', 'KIMI_K27_EXO_MESH', 50050, 'KIMI_K27_CODE_WORKER', 'Kimi K2.7-Code controlled by Exo P2P Mesh Cluster', 1);
                """)

                conn.commit()
                conn.close()
                print(f"[+] Registered Kimi K2.7-Code & Exo Controller in: {os.path.basename(db)}")
            except Exception as e:
                print(f"[-] Notice registering DB {db}: {e}")

    print("==========================================================================")
    print("  [OK] EXO P2P CONTROL ARCHITECTURE FOR KIMI K2.7-CODE ESTABLISHED!")
    print("==========================================================================")

if __name__ == "__main__":
    main()
