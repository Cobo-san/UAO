#!/usr/bin/env python3
"""
SQLite WAL Database Build Optimizer & Performance Review Script
Runs PRAGMA optimize, ANALYZE, and WAL checkpointing across all binary databases.
"""

import os
import sys
import sqlite3
import time
import platform

def get_current_os():
    return platform.system()

def get_db_paths():
    if get_current_os() == "Windows":
        return [
            r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\synaptic_matrix\universal_synaptic_matrix.sqlite",
            r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\Parallel_Synaptic_Database_Matrix\universal_synaptic_matrix.sqlite"
        ]
    else:
        return [
            "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/synaptic_matrix/universal_synaptic_matrix.sqlite",
            "/mnt/c/Users/Monica Fugazi/GoogleDrive_sounddharma/Parallel_Synaptic_Database_Matrix/universal_synaptic_matrix.sqlite"
        ]

def optimize_database(db_path):
    if not os.path.exists(db_path):
        print(f"[!] Database path not found: {db_path}")
        return False

    print(f"[*] Optimizing SQLite WAL Database: {db_path}")
    start_time = time.time()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # WAL Checkpoint
        cursor.execute("PRAGMA wal_checkpoint(FULL);")
        
        # Analyze & Index Optimization
        cursor.execute("ANALYZE;")
        cursor.execute("PRAGMA optimize;")
        
        # Cache Size Optimization (64MB RAM cache)
        cursor.execute("PRAGMA cache_size = -64000;")
        
        conn.commit()
        conn.close()
        
        elapsed_ms = (time.time() - start_time) * 1000
        size_kb = os.path.getsize(db_path) / 1024
        print(f"  [+] Optimization Complete in {elapsed_ms:.2f} ms | Database Size: {size_kb:.2f} KB")
        return True
    except Exception as e:
        print(f"  [!] Optimization error: {e}")
        return False

def main():
    print("=== SQLite WAL Build Optimization & Maintenance Audit ===")
    paths = get_db_paths()
    for db in paths:
        optimize_database(db)
    print("[OK] BUILD OPTIMIZATION & DATABASE MAINTENANCE COMPLETED!")

if __name__ == "__main__":
    main()
