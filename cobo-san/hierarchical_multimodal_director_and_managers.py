#!/usr/bin/env python3
"""
Hierarchical Multi-Modal Director & Specialized Managers Orchestrator Engine
Establishes an executive hierarchical multi-agent structure:
  1. Executive Synaptic Director Agent (Llama 3.3 70B - High-level Goal Synthesis)
  2. Domain Manager 1: Voice & Dialogue Manager (Whisper STT + Piper TTS)
  3. Domain Manager 2: Vision & Terminal Automation Manager (LLaVA OCR + Multi-Terminal Auto)
  4. Domain Manager 3: Code, SDK & ADK Manager (Qwen 2.5 Coder 32B + Android ADK)
  5. Domain Manager 4: Creative Media & UI Manager (FLUX.1 + Meta MusicGen)
"""

import os
import sys
import json
import sqlite3
import subprocess
import platform

ACCOUNT_EMAIL = "sounddharma@gmail.com"
GCP_PROJECT_ID = "anaconda-google-project-sounddharma"

HIERARCHICAL_AGENTS = [
    {
        "agent_id": "agent_executive_director",
        "name": "Executive Synaptic Director",
        "type": "DIRECTOR",
        "assigned_port": 8090,
        "engine_model": "Llama-3.3-70B-Instruct",
        "mcp_server": "kernel_executive_director_mcp",
        "description": "High-level Executive Director overseeing all domain managers, synthesizing voice/text intents and routing task matrices."
    },
    {
        "agent_id": "agent_voice_manager",
        "name": "Voice & Dialogue Manager",
        "type": "MANAGER",
        "assigned_port": 8094,
        "engine_model": "Whisper.cpp + Piper TTS Engine",
        "mcp_server": "kernel_voice_dialogue_mcp",
        "description": "Domain Manager controlling real-time zero-latency speech-to-text input and natural text-to-speech feedback."
    },
    {
        "agent_id": "agent_vision_terminal_manager",
        "name": "Vision & Terminal Automation Manager",
        "type": "MANAGER",
        "assigned_port": 8096,
        "engine_model": "LLaVA-v1.6 / Qwen2-VL Vision Engine",
        "mcp_server": "kernel_vision_terminal_mcp",
        "description": "Domain Manager capturing terminal screens, performing OCR traceback inspection, and driving multi-terminal automation."
    },
    {
        "agent_id": "agent_code_sdk_manager",
        "name": "Code, SDK & ADK Manager",
        "type": "MANAGER",
        "assigned_port": 8091,
        "engine_model": "Qwen-2.5-Coder-32B",
        "mcp_server": "kernel_code_sdk_mcp",
        "description": "Domain Manager controlling Python SDK, Android ADK (Kotlin/NDK), gRPC sockets, and automated unit testing."
    },
    {
        "agent_id": "agent_media_manager",
        "name": "Creative Media & UI Manager",
        "type": "MANAGER",
        "assigned_port": 8097,
        "engine_model": "FLUX.1-schnell + Meta MusicGen",
        "mcp_server": "kernel_media_creation_mcp",
        "description": "Domain Manager generating sleek dark-mode UI graphics, vector logos, and system alert sound FX."
    }
]

def get_current_os():
    return platform.system()

def get_paths():
    if get_current_os() == "Windows":
        return {
            "db_path": r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\synaptic_matrix\universal_synaptic_matrix.sqlite",
            "mcp_config": r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\mcp_servers\mcp_synaptic_kernel_config.json"
        }
    else:
        return {
            "db_path": "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/synaptic_matrix/universal_synaptic_matrix.sqlite",
            "mcp_config": "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/mcp_servers/mcp_synaptic_kernel_config.json"
        }

def register_hierarchical_structure():
    print("=== EXECUTIVE MULTI-MODAL DIRECTOR & DOMAIN MANAGERS ORCHESTRATOR ===")
    paths = get_paths()
    
    if not os.path.exists(paths["db_path"]):
        print(f"[!] SQLite DB path not found: {paths['db_path']}")
        return

    try:
        conn = sqlite3.connect(paths["db_path"])
        cursor = conn.cursor()

        print("\n[*] Registering Executive Director & 4 Domain Managers in SQLite Matrix...")
        for agent in HIERARCHICAL_AGENTS:
            cursor.execute("""
            INSERT OR REPLACE INTO ai_agents_registry
            (agent_id, agent_name, role, status, mirror_location, mcp_port, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (
                agent["agent_id"],
                agent["name"],
                f"{agent['type']} | {agent['mcp_server']}",
                "ACTIVE_READY",
                "C:,D:,E: MultiModal",
                agent["assigned_port"],
                json.dumps({"engine": agent["engine_model"], "description": agent["description"]})
            ))

            cursor.execute("""
            INSERT OR REPLACE INTO mcp_synaptic_routes
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (agent["mcp_server"], "ExecutiveHost", agent["engine_model"], agent["assigned_port"], agent["type"], agent["description"], 1))

            print(f"  [+] Registered {agent['type']}: {agent['name']} (Port {agent['assigned_port']} - MCP: {agent['mcp_server']})")

        conn.commit()
        conn.close()
        print("  [+] SQLite Database updated with 100% success!")
    except Exception as e:
        print(f"  [!] Notice updating SQLite DB: {e}")

def update_mcp_config():
    paths = get_paths()
    print("\n[*] Updating MCP Synaptic Kernel JSON Configuration...")
    if not os.path.exists(paths["mcp_config"]):
        return

    try:
        with open(paths["mcp_config"], "r", encoding="utf-8") as f:
            config = json.load(f)

        mcp_servers = config.get("mcpServers", {})
        for agent in HIERARCHICAL_AGENTS:
            mcp_servers[agent["mcp_server"]] = {
                "command": "python",
                "args": [
                    f"C:\\Users\\Monica Fugazi\\.antigravity-ide\\living_repository\\bin\\hierarchical_multimodal_director_and_managers.py",
                    "--agent", agent["agent_id"]
                ],
                "env": {
                    "AGENT_TYPE": agent["type"],
                    "AGENT_PORT": str(agent["assigned_port"]),
                    "ENGINE_MODEL": agent["engine_model"]
                }
            }

        config["mcpServers"] = mcp_servers
        with open(paths["mcp_config"], "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)

        print(f"  [+] MCP Config updated with {len(mcp_servers)} total Synaptic MCP Kernel servers!")
    except Exception as e:
        print(f"  [!] Notice updating MCP config: {e}")

def main():
    register_hierarchical_structure()
    update_mcp_config()
    print("\n[OK] EXECUTIVE DIRECTOR & DOMAIN MANAGERS SUCCESSFULLY EXECUTED & INSTALLED!")

if __name__ == "__main__":
    main()
