#!/usr/bin/env python3
"""
Dynamic Skill Creation & Registration Framework
Enables creating, formatting, cataloging, and registering new agent skills on the fly.
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

def create_dynamic_skill(skill_name, description, markdown_instructions):
    repo_dir = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository"
    if get_current_os() != "Windows":
        repo_dir = "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository"

    skills_dir = os.path.join(repo_dir, "skills")
    skill_folder = os.path.join(skills_dir, skill_name.replace("-", "_"))
    os.makedirs(skill_folder, exist_ok=True)

    skill_file = os.path.join(skill_folder, "SKILL.md")
    
    skill_content = f"""---
name: {skill_name}
description: {description}
---

{markdown_instructions}
"""
    with open(skill_file, "w", encoding="utf-8") as f:
        f.write(skill_content)

    # Update skills_manifest.json
    manifest_path = os.path.join(skills_dir, "skills_manifest.json")
    skills_data = []
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                skills_data = data.get("skills", [])
        except Exception:
            skills_data = []

    # Update or add skill
    existing = False
    for s in skills_data:
        if s.get("name") == skill_name:
            s["description"] = description
            s["path"] = skill_file
            s["updated_timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            existing = True
            break
    
    if not existing:
        skills_data.append({
            "name": skill_name,
            "path": skill_file,
            "description": description,
            "created_timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "status": "ACTIVE_REGISTERED"
        })

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({"total_skills": len(skills_data), "skills": skills_data}, f, indent=2)

    # Register in SQLite Database
    db_path = get_db_path()
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS custom_skills_registry (skill_name TEXT PRIMARY KEY, skill_path TEXT, description TEXT, registered_timestamp TEXT);")
        cursor.execute("INSERT OR REPLACE INTO custom_skills_registry VALUES (?, ?, ?, ?);",
                       (skill_name, skill_file, description, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
        conn.commit()
        conn.close()

    print(f"[+] Dynamic Skill Successfully Created & Cataloged: {skill_name} ({skill_file})")
    return skill_file

def main():
    print("=== DYNAMIC SKILL CREATION FRAMEWORK ENABLED ===")
    
    # Register an example dynamic skill: Quantum & Math Compute Skill
    sample_desc = "Skill for executing Google Quantum AI simulations (Cirq, OpenFermion) and Intel oneAPI math acceleration."
    sample_instructions = """# Quantum & Math Compute Skill Instructions

Use this skill when simulating quantum circuits or executing high-performance linear algebra and matrix math.

---

## ⚛️ Quantum Simulation Tools

- **Google Quantum AI Test**: `python C:\\Users\\Monica Fugazi\\.antigravity-ide\\living_repository\\bin\\test_google_quantum_ecosystem.py`
- **Cirq Bell State Simulator**: `python C:\\Users\\Monica Fugazi\\.antigravity-ide\\living_repository\\bin\\test_cirq_sim.py`

---

## 🧮 Upper Math Tools

- **Intel oneMKL Acceleration**: `python -c "import mkl; print('oneMKL Version:', mkl.get_version_string())"`
"""
    create_dynamic_skill("quantum-and-math-compute", sample_desc, sample_instructions)
    print("[OK] DYNAMIC SKILL CREATION SYSTEM FULLY ENABLED & ACTIVE!")

if __name__ == "__main__":
    main()
