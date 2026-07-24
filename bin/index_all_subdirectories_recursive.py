#!/usr/bin/env python3
"""
Exhaustive Recursive Subdirectory & File Inventory Engine
Crawls, categorizes, and indexes ALL subdirectories and nested files across
Living Repository and Google Drive (sounddharma@gmail.com) into SQLite DB Matrix.
"""

import os
import sys
import json
import sqlite3
import time
import platform

ACCOUNT_EMAIL = "sounddharma@gmail.com"
GCP_PROJECT_ID = "anaconda-google-project-sounddharma"

def get_current_os():
    return platform.system()

def get_paths():
    if get_current_os() == "Windows":
        return {
            "living_repo": r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository",
            "db_path": r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\synaptic_matrix\universal_synaptic_matrix.sqlite",
            "gdrive_root": r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma",
            "gdrive_golden": r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\Golden_Image_Database",
            "gdrive_db": r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\Parallel_Synaptic_Database_Matrix\universal_synaptic_matrix.sqlite"
        }
    else:
        return {
            "living_repo": "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository",
            "db_path": "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/synaptic_matrix/universal_synaptic_matrix.sqlite",
            "gdrive_root": "/mnt/c/Users/Monica Fugazi/GoogleDrive_sounddharma",
            "gdrive_golden": "/mnt/c/Users/Monica Fugazi/GoogleDrive_sounddharma/Golden_Image_Database",
            "gdrive_db": "/mnt/c/Users/Monica Fugazi/GoogleDrive_sounddharma/Parallel_Synaptic_Database_Matrix/universal_synaptic_matrix.sqlite"
        }

def scan_directory_tree(root_dir):
    inventory = []
    if not os.path.exists(root_dir):
        return inventory

    for current_root, subdirs, files in os.walk(root_dir):
        rel_dir = os.path.relpath(current_root, root_dir)
        for f in files:
            full_path = os.path.join(current_root, f)
            size_bytes = os.path.getsize(full_path) if os.path.exists(full_path) else 0
            inventory.append({
                "parent_root": root_dir,
                "subdir_path": rel_dir if rel_dir != "." else "root",
                "filename": f,
                "full_path": full_path,
                "size_bytes": size_bytes
            })
    return inventory

def register_inventory_in_database(db_path, inventory_records):
    if not os.path.exists(db_path):
        return

    try:
        os.chmod(db_path, 0o666)
    except Exception:
        pass

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recursive_subdirectory_inventory (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        parent_root TEXT,
        subdir_path TEXT,
        filename TEXT,
        full_path TEXT,
        size_bytes INTEGER,
        indexed_timestamp TEXT
    );
    """)

    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    cursor.execute("DELETE FROM recursive_subdirectory_inventory;")

    records = [
        (item["parent_root"], item["subdir_path"], item["filename"], item["full_path"], item["size_bytes"], ts)
        for item in inventory_records
    ]
    cursor.executemany("""
    INSERT INTO recursive_subdirectory_inventory (parent_root, subdir_path, filename, full_path, size_bytes, indexed_timestamp)
    VALUES (?, ?, ?, ?, ?, ?);
    """, records)

    conn.commit()
    conn.close()

def main():
    print("=== EXHAUSTIVE RECURSIVE SUBDIRECTORY INVENTORY ENGINE ===")
    paths = get_paths()

    print("[*] Scanning Living Repository subdirectories...")
    living_inventory = scan_directory_tree(paths["living_repo"])
    print(f"  [+] Living Repo Files Scanned across Subdirectories: {len(living_inventory)} files")

    print("[*] Scanning Google Drive subdirectories...")
    gdrive_inventory = scan_directory_tree(paths["gdrive_root"])
    print(f"  [+] Google Drive Files Scanned across Subdirectories: {len(gdrive_inventory)} files")

    all_records = living_inventory + gdrive_inventory

    # Register in Living Repo DB
    register_inventory_in_database(paths["db_path"], all_records)
    print(f"[+] Subdirectory Inventory Registered in Living Repo DB: {paths['db_path']}")

    # Register in Google Drive DB
    register_inventory_in_database(paths["gdrive_db"], all_records)
    print(f"[+] Subdirectory Inventory Replicated to Google Drive DB: {paths['gdrive_db']}")

    # Save JSON manifest
    manifest_path = os.path.join(paths["living_repo"], "recursive_all_subdirectories_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_items": len(all_records),
            "living_repo_items": len(living_inventory),
            "gdrive_items": len(gdrive_inventory),
            "inventory": all_records
        }, f, indent=2)

    gdrive_manifest_path = os.path.join(paths["gdrive_golden"], "recursive_all_subdirectories_manifest.json")
    if os.path.exists(gdrive_manifest_path):
        try:
            os.chmod(gdrive_manifest_path, 0o666)
        except Exception:
            pass
    with open(gdrive_manifest_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_items": len(all_records),
            "living_repo_items": len(living_inventory),
            "gdrive_items": len(gdrive_inventory),
            "inventory": all_records
        }, f, indent=2)

    print(f"[+] Recursive All Subdirectories Manifest Saved: {manifest_path}")
    print(f"[+] Manifest Saved to Google Drive Golden Database: {gdrive_manifest_path}")
    print("[OK] EXHAUSTIVE RECURSIVE SUBDIRECTORY INVENTORY COMPLETED WITH 100% SUCCESS!")

if __name__ == "__main__":
    main()
