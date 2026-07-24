#!/usr/bin/env python3
"""
Universal Cross-OS Binary IPC, Storage & Metadata Sync Engine
Includes Google Drive, NVMe Drives, LLM DB Storage, Living Repository,
and Project Data across Windows, WSL, and all Linux Distros in uniform format.
"""

import os
import sys
import json
import struct
import sqlite3
import platform
import time
from pathlib import Path

# Dual NVMe Drive, Google Drive & Core Path Registry
WINDOWS_PRIMARY_NVME = r"C:\AI_Dedicated_Storage_1TB"
WINDOWS_SECONDARY_NVME = r"D:\AI_Dedicated_Storage_Secondary"
WINDOWS_GOOGLE_DRIVE = r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma"
WINDOWS_LIVING_REPO = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository"
WINDOWS_AI_BRAIN = r"C:\Users\Monica Fugazi\.gemini\antigravity-cli\brain"

POSIX_PRIMARY_NVME = "/mnt/c/AI_Dedicated_Storage_1TB"
POSIX_SECONDARY_NVME = "/mnt/d/AI_Dedicated_Storage_Secondary"
POSIX_GOOGLE_DRIVE = "/mnt/c/Users/Monica Fugazi/GoogleDrive_sounddharma"
POSIX_LIVING_REPO = "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository"
POSIX_AI_BRAIN = "/mnt/c/Users/Monica Fugazi/.gemini/antigravity-cli/brain"

VAR_PRIMARY = "/var/ai_storage_primary"
VAR_SECONDARY = "/var/ai_storage_secondary"
VAR_GDRIVE = "/var/google_drive_sounddharma"
VAR_LIVING = "/var/living_repository"
VAR_BRAIN = "/var/ai_brain"

def get_current_os():
    return platform.system()

def get_native_paths():
    current_os = get_current_os()
    if current_os == "Windows":
        return {
            "primary": WINDOWS_PRIMARY_NVME,
            "secondary": WINDOWS_SECONDARY_NVME,
            "gdrive": WINDOWS_GOOGLE_DRIVE,
            "living_repo": WINDOWS_LIVING_REPO,
            "brain": WINDOWS_AI_BRAIN,
            "golden_db": os.path.join(WINDOWS_GOOGLE_DRIVE, "Golden_Image_Database"),
            "synaptic_drive": os.path.join(WINDOWS_GOOGLE_DRIVE, "Parallel_Synaptic_Database_Matrix"),
            "snapshots": os.path.join(WINDOWS_GOOGLE_DRIVE, "Snapshots_Reversion_Archive"),
            "staging": os.path.join(WINDOWS_GOOGLE_DRIVE, "Staging_Build_15Day_Test")
        }
    else:
        # Linux / WSL
        gdrive = POSIX_GOOGLE_DRIVE if os.path.exists(POSIX_GOOGLE_DRIVE) else VAR_GDRIVE
        return {
            "primary": POSIX_PRIMARY_NVME if os.path.exists(POSIX_PRIMARY_NVME) else VAR_PRIMARY,
            "secondary": POSIX_SECONDARY_NVME if os.path.exists(POSIX_SECONDARY_NVME) else VAR_SECONDARY,
            "gdrive": gdrive,
            "living_repo": POSIX_LIVING_REPO if os.path.exists(POSIX_LIVING_REPO) else VAR_LIVING,
            "brain": POSIX_AI_BRAIN if os.path.exists(POSIX_AI_BRAIN) else VAR_BRAIN,
            "golden_db": os.path.join(gdrive, "Golden_Image_Database"),
            "synaptic_drive": os.path.join(gdrive, "Parallel_Synaptic_Database_Matrix"),
            "snapshots": os.path.join(gdrive, "Snapshots_Reversion_Archive"),
            "staging": os.path.join(gdrive, "Staging_Build_15Day_Test")
        }

def build_universal_binary_ipc_db(target_db_path):
    """
    Creates/Initializes SQLite WAL binary database accessible across all OS distros.
    Includes uniform tables for NVMe, Google Drive, LLM DB Storage, and Project Repos.
    """
    if os.path.exists(target_db_path):
        try:
            os.chmod(target_db_path, 0o666)
        except Exception:
            pass

    conn = sqlite3.connect(target_db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")
    
    # Table 1: Storage Drives & Repos Metadata
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS universal_storage_registry (
        storage_id TEXT PRIMARY KEY,
        domain_name TEXT,
        windows_path TEXT,
        posix_symlink TEXT,
        capacity_gb REAL,
        status TEXT,
        format_type TEXT
    );
    """)

    # Table 2: LLM Databases & Model Storage
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS llm_database_registry (
        model_id TEXT PRIMARY KEY,
        model_name TEXT,
        storage_location TEXT,
        file_size_gb REAL,
        mmap_protocol TEXT,
        status TEXT
    );
    """)

    # Table 3: Usage Data & Metrics
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usage_metadata (
        metric_id TEXT PRIMARY KEY,
        os_distro TEXT,
        timestamp_utc TEXT,
        cpu_usage_pct REAL,
        ram_used_gb REAL,
        nvme_c_read_mbps REAL,
        nvme_d_read_mbps REAL,
        gdrive_sync_status TEXT,
        payload_blob BLOB
    );
    """)
    
    # Table 4: AI Agents Registry
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_agents_registry (
        agent_id TEXT PRIMARY KEY,
        agent_name TEXT,
        role TEXT,
        status TEXT,
        mirror_location TEXT,
        mcp_port INTEGER,
        metadata_json TEXT
    );
    """)

    conn.commit()
    return conn

def pack_binary_ipc_header(magic=0x41494756, version=2, total_agents=6, total_storages=5):
    """
    Packs a 32-byte binary IPC header struct.
    Magic: 'AIGV' (0x41494756)
    """
    ts = time.time()
    header_bin = struct.pack("<IHHId12s", magic, version, total_agents, total_storages, ts, b"\x00" * 12)
    return header_bin

def unpack_binary_ipc_header(header_bin):
    magic, version, total_agents, total_storages, ts, reserved = struct.unpack("<IHHId12s", header_bin)
    return {
        "magic": hex(magic),
        "version": version,
        "total_agents": total_agents,
        "total_storages": total_storages,
        "timestamp": ts
    }

def main():
    paths = get_native_paths()
    print(f"[*] Detected Operating System: {get_current_os()}")
    print(f"[*] Primary NVMe Path: {paths['primary']}")
    print(f"[*] Secondary NVMe Path: {paths['secondary']}")
    print(f"[*] Google Drive Path: {paths['gdrive']}")
    print(f"[*] Living Repository: {paths['living_repo']}")

    # Setup SQLite Binary IPC DB inside living_repository/synaptic_matrix/
    repo_dir = Path(paths["living_repo"])
    matrix_dir = repo_dir / "synaptic_matrix"
    matrix_dir.mkdir(parents=True, exist_ok=True)
    db_path = matrix_dir / "universal_synaptic_matrix.sqlite"
    
    conn = build_universal_binary_ipc_db(str(db_path))
    print(f"[+] Universal SQLite Binary IPC Database Initialized: {db_path}")

    # Also duplicate DB into Google Drive for cloud redundancy
    gdrive_matrix_dir = Path(paths["synaptic_drive"])
    gdrive_matrix_dir.mkdir(parents=True, exist_ok=True)
    gdrive_db_path = gdrive_matrix_dir / "universal_synaptic_matrix.sqlite"
    conn_gdrive = build_universal_binary_ipc_db(str(gdrive_db_path))
    conn_gdrive.close()
    print(f"[+] Google Drive Cloud Binary Database Initialized: {gdrive_db_path}")

    # Pack 32-byte binary header
    header = pack_binary_ipc_header()
    bin_header_file = matrix_dir / "universal_ipc_state.bin"
    if bin_header_file.exists():
        try:
            os.chmod(str(bin_header_file), 0o666)
        except Exception:
            pass

    with open(bin_header_file, "wb") as f:
        f.write(header)
    
    gdrive_header_file = gdrive_matrix_dir / "universal_ipc_state.bin"
    if gdrive_header_file.exists():
        try:
            os.chmod(str(gdrive_header_file), 0o666)
        except Exception:
            pass

    with open(gdrive_header_file, "wb") as f:
        f.write(header)
    print(f"[+] Universal Binary Header State Synchronized to Living Repo & Google Drive ({len(header)} bytes)")

    # Verify unpack
    with open(bin_header_file, "rb") as f:
        unpacked = unpack_binary_ipc_header(f.read())
    print(f"[+] Verified Binary Header Unpack: {unpacked}")

    # Populate Universal Storage Registry
    cursor = conn.cursor()
    storages = [
        ("primary_nvme", "Sabrent Rocket 1TB NVMe", WINDOWS_PRIMARY_NVME, VAR_PRIMARY, 1000.0, "ACTIVE", "PROT_READ_UNIFORM"),
        ("secondary_nvme", "Samsung 970 EVO 500GB NVMe", WINDOWS_SECONDARY_NVME, VAR_SECONDARY, 500.0, "ACTIVE", "PROT_READ_UNIFORM"),
        ("google_drive", "Google Drive Cloud Storage", WINDOWS_GOOGLE_DRIVE, VAR_GDRIVE, 2000.0, "ACTIVE_SYNCED", "UNIFORM_CLOUD_REDUNDANT"),
        ("living_repo", "Living Repository Active Workspace", WINDOWS_LIVING_REPO, VAR_LIVING, 100.0, "AUTO_MOUNTED", "UNIFORM_WORKSPACE"),
        ("ai_brain", "AI Agents Brain & Memory Logs", WINDOWS_AI_BRAIN, VAR_BRAIN, 50.0, "ACTIVE", "UNIFORM_MEMORY_LOGS")
    ]
    cursor.executemany("INSERT OR REPLACE INTO universal_storage_registry VALUES (?,?,?,?,?,?,?)", storages)

    # Populate LLM Database Registry
    llm_models = [
        ("llama_3_3_70b_primary", "Llama 3.3 70B Instruct GGUF (C:)", paths['primary'] + r"\models_gguf\llama-3.3-70b-instruct.gguf", 42.52, "PROT_READ_MMAP", "ACTIVE"),
        ("llama_3_3_70b_secondary", "Llama 3.3 70B Instruct GGUF (D:)", paths['secondary'] + r"\models_gguf_mirror\llama-3.3-70b-instruct.gguf", 42.52, "PROT_READ_MMAP", "ACTIVE")
    ]
    cursor.executemany("INSERT OR REPLACE INTO llm_database_registry VALUES (?,?,?,?,?,?)", llm_models)

    # Populate Agent Registry in DB
    agents = [
        ("llama_native_70b_agent", "Llama 3.3 70B Local Engine", "Local Inference", "PASSED", paths['secondary'], 8080, '{"drive": "D:"}'),
        ("master_assembly_orchestrator", "Assembly Orchestrator", "Cluster Leader", "PASSED", paths['primary'], 8081, '{"role": "Leader"}'),
        ("skill_cluster_manager_mirror1", "Mirror 1 Skill Manager", "47 Skills Manager", "PASSED", paths['primary'], 8082, '{"skills": 47}'),
        ("vector_cluster_manager_mirror2", "Mirror 2 Vector Manager", "62 Vector Nodes", "PASSED", paths['secondary'], 8083, '{"vectors": 62}'),
        ("settings_cluster_manager_mirror3", "Mirror 3 Env Manager", "741 Extensions Manager", "PASSED", paths['primary'], 8084, '{"extensions": 741}'),
        ("agent_rag", "Agent RAG Vector Search", "RAG Cosine Engine", "PASSED", paths['primary'], 8085, '{"cosine_min": 0.81}')
    ]
    cursor.executemany("INSERT OR REPLACE INTO ai_agents_registry VALUES (?,?,?,?,?,?,?)", agents)
    conn.commit()
    conn.close()

    print("[OK] UNIFORM GOOGLE DRIVE, NVME, REPOS & LLM DB STORAGE SYNC INITIALIZED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
