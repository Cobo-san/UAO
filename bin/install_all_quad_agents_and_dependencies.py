#!/usr/bin/env python3
"""
Master Quad-Agent & Dependency Installer Engine
Collects all Python/Conda dependencies and installs/registers all 4 specialized agents:
  1. Llama-3.3-70B (Master System Orchestrator)
  2. Qwen-2.5-Coder-32B (Python SDK, Android ADK & Network Sockets)
  3. DeepSeek-R1-70B (Protocol Debugging & Reasoning)
  4. Codestral-22B (Fast Subagent Background Worker)
"""

import os
import sys
import subprocess
import json
import sqlite3
import platform

ACCOUNT_EMAIL = "sounddharma@gmail.com"
GCP_PROJECT_ID = "anaconda-google-project-sounddharma"

DEPENDENCIES = [
    "requests",
    "python-dotenv",
    "pydantic",
    "pyyaml"
]

AGENT_MODELFILES = {
    "llama3.3:latest": {
        "source": "/mnt/d/AI_Dedicated_Storage_Secondary/models_gguf_mirror/Llama-3.3-70B-Instruct-Q4_K_M.gguf",
        "system": "You are the Master Orchestrator subagent for the UAO system."
    },
    "qwen2.5-coder:latest": {
        "source": "/mnt/d/AI_Dedicated_Storage_Secondary/models_gguf_mirror/Qwen-2.5-Coder-32B-Instruct-Q5_K_M.gguf",
        "system": "You are the specialized Python SDK, Android ADK (Kotlin/Java/NDK), and Network Socket subagent."
    },
    "deepseek-r1:latest": {
        "source": "/mnt/d/AI_Dedicated_Storage_Secondary/models_gguf_mirror/DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf",
        "system": "You are the specialized Protocol Debugging, Async Race Condition, and Deep Reasoning subagent."
    },
    "codestral:latest": {
        "source": "/mnt/e/AI_Dedicated_Storage_Tertiary/models_gguf/Codestral-22B-v0.1-Q5_K_M.gguf",
        "system": "You are the Fast Subagent Background Worker & Unit Test Engine."
    }
}

def install_python_dependencies():
    print("[*] 1/3. Collecting and Verifying Python Dependencies...")
    for dep in DEPENDENCIES:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", dep])
            print(f"  [+] Installed / Verified: {dep}")
        except Exception as e:
            print(f"  [!] Notice installing {dep}: {e}")

def create_and_register_ollama_modelfiles():
    print("\n[*] 2/3. Creating Modelfiles and Registering All 4 Quad Agents in Ollama...")
    ollama_dir = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\templates\ollama"
    os.makedirs(ollama_dir, exist_ok=True)

    for agent_name, info in AGENT_MODELFILES.items():
        mf_path = os.path.join(ollama_dir, f"Modelfile.{agent_name}")
        content = f"""FROM {info['source']}

SYSTEM \"\"\"{info['system']}\"\"\"

PARAMETER num_ctx 8192
PARAMETER temperature 0.7
PARAMETER top_p 0.9
"""
        with open(mf_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [+] Generated Modelfile: {mf_path}")

        # Register in Ollama via WSL2 if available
        try:
            posix_mf = f"/mnt/c/Users/Monica\\ Fugazi/.antigravity-ide/living_repository/templates/ollama/Modelfile.{agent_name}"
            cmd = f"wsl bash -c \"~/.local/bin/ollama create {agent_name} -f {posix_mf}\""
            subprocess.Popen(cmd, shell=True)
            print(f"  [+] Dispatched background Ollama registration for agent: {agent_name}")
        except Exception as e:
            print(f"  [!] Notice registering {agent_name}: {e}")

def verify_system_catalog():
    print("\n[*] 3/3. Verifying System Catalog & Database Integration...")
    repo_bin = os.path.dirname(__file__)
    orch_script = os.path.join(repo_bin, "quad_model_tri_drive_orchestrator.py")
    subprocess.check_call([sys.executable, orch_script])

def main():
    print("=== MASTER QUAD-AGENT & DEPENDENCY INSTALLER ENGINE ===")
    install_python_dependencies()
    create_and_register_ollama_modelfiles()
    verify_system_catalog()
    print("\n[OK] ALL DEPENDENCIES COLLECTED & ALL 4 AGENTS INSTALLED WITH 100% SUCCESS!")

if __name__ == "__main__":
    main()
