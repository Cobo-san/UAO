#!/usr/bin/env python3
import sqlite3
import json

def register_supreme_architect():
    db_path = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\synaptic_matrix\universal_synaptic_matrix.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    agent_id = "agent_uao_supreme_architect"
    agent_name = "UAO Supreme Assembly Architect"
    role_spec = "SUPREME_DIRECTOR | kernel_uao_supreme_mcp"
    health = "ACTIVE_READY"
    target = "C:,D:,E: MultiModal"
    port = 8100
    metadata = {
        "engine": "Llama-3.3-70B-Instruct (Master Node)",
        "description": "Supreme Unified Assembly Orchestrator. Understands overarching user direction, tracks user corrections and errors, and dynamically overrides and directs all other Executive and Domain Managers to ensure absolute Unified Assembly."
    }

    cursor.execute("""
    INSERT OR REPLACE INTO ai_agents_registry 
    (agent_id, agent_name, role, status, mirror_location, mcp_port, metadata_json)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (agent_id, agent_name, role_spec, health, target, port, json.dumps(metadata)))

    conn.commit()
    conn.close()
    
    print(f"[+] Successfully Registered: {agent_name} on Port {port}")
    print(f"    Role: {role_spec}")
    print(f"    Mission: Realize corrections, enhance build, and direct all sub-managers under UAO.")

if __name__ == "__main__":
    register_supreme_architect()
