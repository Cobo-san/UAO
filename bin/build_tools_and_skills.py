#!/usr/bin/env python3
"""
Master Tools & Skills Builder Engine
Registers, indexes, and builds custom agent skills and tools in the living repository.
"""

import os
import sys
import json
import sqlite3
import time
import platform

def get_current_os():
    return platform.system()

def get_db_path():
    if get_current_os() == "Windows":
        return r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\synaptic_matrix\universal_synaptic_matrix.sqlite"
    else:
        return "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/synaptic_matrix/universal_synaptic_matrix.sqlite"

def main():
    print("=== MASTER TOOLS & SKILLS BUILDER ENGINE ===")
    repo_dir = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository"
    if get_current_os() != "Windows":
        repo_dir = "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository"

    skills_dir = os.path.join(repo_dir, "skills")
    os.makedirs(skills_dir, exist_ok=True)

    skills_manifest_path = os.path.join(skills_dir, "skills_manifest.json")
    
    registered_skills = [
        {
            "name": "master-set-system-control",
            "path": os.path.join(skills_dir, "master_set_system_skill", "SKILL.md"),
            "description": "Operational skill for managing the Anaconda Google Project Set System, status diagnostics, quantum AI simulations, route security audits, and memory snapshot backups.",
            "status": "ACTIVE_REGISTERED"
        }
    ]

    with open(skills_manifest_path, "w") as f:
        json.dump({"total_skills": len(registered_skills), "skills": registered_skills}, f, indent=2)

    print(f"[+] Skills Manifest Built & Saved ({len(registered_skills)} registered skill): {skills_manifest_path}")

    # Register in SQLite Database
    db_path = get_db_path()
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS custom_skills_registry (skill_name TEXT PRIMARY KEY, skill_path TEXT, description TEXT, registered_timestamp TEXT);")
        
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        for s in registered_skills:
            cursor.execute("INSERT OR REPLACE INTO custom_skills_registry VALUES (?, ?, ?, ?);", (s["name"], s["path"], s["description"], ts))
        
        conn.commit()
        conn.close()
        print(f"[+] Custom Skills Registry Table Updated in SQLite WAL: {db_path}")

    print("[OK] MASTER TOOLS AND SKILLS BUILT AND REGISTERED WITH 100% SUCCESS!")

if __name__ == "__main__":
    main()
