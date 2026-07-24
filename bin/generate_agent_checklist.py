#!/usr/bin/env python3
"""
Agent System Checklist Generator
Audits all 12 registered Executive Directors, Domain Managers, and Subagent Workers
in the SQLite WAL matrix and prints the complete live checklist.
"""

import sqlite3
import os
import platform

def generate_checklist():
    db_path = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\synaptic_matrix\universal_synaptic_matrix.sqlite"
    if platform.system() != "Windows":
        db_path = "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/synaptic_matrix/universal_synaptic_matrix.sqlite"

    print("=== UAO EXECUTIVE & DOMAIN AGENT CHECKLIST ===")

    if not os.path.exists(db_path):
        print("  [!] SQLite Database not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT agent_id, agent_name, role, status, mcp_port, metadata_json FROM ai_agents_registry")
    agents = cursor.fetchall()
    conn.close()

    print(f"\n[+] Total Registered Agents in SQLite Matrix: {len(agents)}")
    print("--------------------------------------------------------------------------")
    for a in agents:
        agent_id, name, role, status, port, meta = a
        print(f"  [OK] [{status}] {name}")
        print(f"      - ID: {agent_id}")
        print(f"      - Role: {role}")
        print(f"      - Synaptic MCP Port: {port}")
    print("--------------------------------------------------------------------------")

if __name__ == "__main__":
    generate_checklist()
