#!/usr/bin/env python3
"""
Master Detailed Inventory Report Generator for All Mirror Nodes and Instances
Queries SQLite WAL tables and prints a clean, structured master report.
"""

import os
import sys
import sqlite3
import platform

def get_current_os():
    return platform.system()

def get_db_path():
    if get_current_os() == "Windows":
        return r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\synaptic_matrix\universal_synaptic_matrix.sqlite"
    else:
        return "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/synaptic_matrix/universal_synaptic_matrix.sqlite"

def main():
    print("=== MASTER DETAILED INVENTORY: ALL MIRROR NODES & INSTANCES ===")
    db_path = get_db_path()

    if not os.path.exists(db_path):
        print("[-] Database missing.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Zero-Cost Instances Registry
    cursor.execute("SELECT instance_id, provider, region, machine_type, disk_gb, kernel_name, engine_type, mcp_port, monthly_cost FROM zero_cost_instances_registry;")
    instances = cursor.fetchall()

    # 2. Multi-Continent Mirrors Registry
    cursor.execute("SELECT continent, region, provider, monthly_cost, role FROM multi_continent_mirror_registry;")
    continents = cursor.fetchall()

    # 3. Native AI Agents Registry
    cursor.execute("SELECT * FROM ai_agents_registry;")
    agents = cursor.fetchall()

    conn.close()

    print(f"\n===========================================================================")
    print(f"  PART 1: REGISTERED ZERO-COST INSTANCES & SYNAPTIC KERNELS ({len(instances)} INSTANCES)")
    print(f"===========================================================================")
    for idx, inst in enumerate(instances, 1):
        print(f"[{idx}] INSTANCE ID: {inst[0]}")
        print(f"    • Provider & Region : {inst[1]} -> {inst[2]}")
        print(f"    • Hardware Spec     : {inst[3]} ({inst[4]} GB Disk)")
        print(f"    • Synaptic Kernel   : {inst[5]} (Port {inst[7]})")
        print(f"    • Engine Type       : {inst[6]}")
        print(f"    • Monthly Cost      : {inst[8]}")
        print("-" * 75)

    print(f"\n===========================================================================")
    print(f"  PART 2: MULTI-CONTINENT GLOBAL EDGE MIRRORS ({len(continents)} CONTINENTS)")
    print(f"===========================================================================")
    for idx, cont in enumerate(continents, 1):
        print(f"[{idx}] CONTINENT / DOMAIN: {cont[0]}")
        print(f"    • Target Edge Region : {cont[1]}")
        print(f"    • Infrastructure     : {cont[2]}")
        print(f"    • Assigned Role      : {cont[4]}")
        print(f"    • Monthly Cost       : {cont[3]}")
        print("-" * 75)

    print(f"\n===========================================================================")
    print(f"  PART 3: LOCAL NATIVE AI AGENTS & SUBAGENT CLUSTERS ({len(agents)} AGENTS)")
    print(f"===========================================================================")
    for idx, a in enumerate(agents, 1):
        print(f"[{idx}] AGENT ID: {a[0]}")
        print(f"    • Agent Name    : {a[1]}")
        print(f"    • Role Spec     : {a[2]}")
        print(f"    • Storage Target: {a[4]} (Port {a[5]})")
        print(f"    • Health Status : {a[3]}")
        print("-" * 75)

    print("[OK] MASTER DETAILED INVENTORY GENERATED WITH 100% SUCCESS!")

if __name__ == "__main__":
    main()
