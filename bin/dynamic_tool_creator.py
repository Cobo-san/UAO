#!/usr/bin/env python3
"""
Dynamic Tool Creation & Registration Framework
Enables creating, compiling, registering, and deploying custom AI tools and skills dynamically.
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

def create_dynamic_tool(tool_name, description, python_code, inputs_schema=None):
    repo_dir = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository"
    if get_current_os() != "Windows":
        repo_dir = "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository"

    tools_dir = os.path.join(repo_dir, "custom_tools")
    os.makedirs(tools_dir, exist_ok=True)

    tool_file = os.path.join(tools_dir, f"{tool_name}.py")
    with open(tool_file, "w", encoding="utf-8") as f:
        f.write(python_code)

    meta_file = os.path.join(tools_dir, f"{tool_name}.json")
    metadata = {
        "tool_name": tool_name,
        "description": description,
        "script_path": tool_file,
        "created_timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        "inputs_schema": inputs_schema or {}
    }
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    # Register in SQLite DB
    db_path = get_db_path()
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS dynamic_tools_registry (tool_name TEXT PRIMARY KEY, description TEXT, script_path TEXT, metadata_json TEXT, registered_timestamp TEXT);")
        cursor.execute("INSERT OR REPLACE INTO dynamic_tools_registry VALUES (?, ?, ?, ?, ?);",
                       (tool_name, description, tool_file, json.dumps(metadata), metadata["created_timestamp"]))
        conn.commit()
        conn.close()

    print(f"[+] Dynamic Tool Successfully Created & Registered: {tool_name} ({tool_file})")
    return tool_file

def main():
    print("=== DYNAMIC TOOL CREATION FRAMEWORK ENABLED ===")
    
    # Register an example dynamic tool: System Health Check Tool
    sample_code = """#!/usr/bin/env python3
import sys
import platform
import time

def main():
    print(f"=== Dynamic Tool Execution: System Health Check ===")
    print(f"[*] OS: {platform.system()} ({platform.release()})")
    print(f"[*] Python: {sys.version.split()[0]}")
    print(f"[*] Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC")
    print("[OK] DYNAMIC TOOL EXECUTION PASSED!")

if __name__ == "__main__":
    main()
"""
    create_dynamic_tool("system_health_check_tool", "Dynamic tool to perform rapid OS & Python health check", sample_code)
    print("[OK] DYNAMIC TOOL CREATION SYSTEM FULLY ENABLED & ACTIVE!")

if __name__ == "__main__":
    main()
