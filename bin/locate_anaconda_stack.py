#!/usr/bin/env python3
"""
Anaconda AI Platform & Environmental Stack Locator
Prints the exact physical file paths, database tables, API endpoints, and blueprint locations.
"""

import os
import sqlite3
import platform

def locate_anaconda_stack():
    print("=== ANACONDA AI PLATFORM & ENVIRONMENTAL STACK LOCATOR REPORT ===")

    db_path = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\synaptic_matrix\universal_synaptic_matrix.sqlite"
    gdrive_db = r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\Parallel_Synaptic_Database_Matrix\universal_synaptic_matrix.sqlite"

    if platform.system() != "Windows":
        db_path = "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/synaptic_matrix/universal_synaptic_matrix.sqlite"
        gdrive_db = "/mnt/c/Users/Monica Fugazi/GoogleDrive_sounddharma/Parallel_Synaptic_Database_Matrix/universal_synaptic_matrix.sqlite"

    print("\n--- 1. GCP Project & Account Integration ---")
    print("  • GCP Project ID: anaconda-google-project-sounddharma")
    print("  • GCP User Account: sounddharma@gmail.com")
    print(f"  • Primary WAL Database: {db_path} ({'EXISTS' if os.path.exists(db_path) else 'MISSING'})")
    print(f"  • Google Drive Mirror Database: {gdrive_db} ({'EXISTS' if os.path.exists(gdrive_db) else 'MISSING'})")

    print("\n--- 2. Anaconda AI Studio Local Server Endpoint ---")
    print("  • Host Endpoint API: http://localhost:8090/v1")
    print("  • Compatible API: OpenAI-compatible llama.cpp server")

    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("\n--- 3. Registered Anaconda Database Tables & Records ---")
        cursor.execute("SELECT gcp_project_id, account_email, status FROM anaconda_google_project_integration")
        proj = cursor.fetchall()
        for p in proj:
            print(f"  • Project Record: {p[0]} | Account: {p[1]} | Status: {p[2]}")

        cursor.execute("SELECT framework_name, version, status FROM anaconda_framework_integrations")
        fw = cursor.fetchall()
        print(f"\n  • Registered Frameworks ({len(fw)} total):")
        for f in fw:
            print(f"    - {f[0]} v{f[1]} -> Status: {f[2]}")

        cursor.execute("SELECT model_name, file_path, file_size_gb FROM anaconda_llm_catalog LIMIT 5")
        cat = cursor.fetchall()
        print(f"\n  • Mapped LLM Catalog Sample (18 total):")
        for c in cat:
            print(f"    - {c[0]} ({c[2]} GB) -> Path: {c[1]}")

        conn.close()

    print("\n--- 4. Master Source Files & Blueprints ---")
    print("  • Integration Script: living_repository/bin/anaconda_full_ecosystem_integration.py")
    print("  • Master Blueprint: living_repository/cobo-san/anaconda_master_ai_platform_stack.md")

    print("\n[OK] ANACONDA STACK LOCATOR AUDIT COMPLETE!")

if __name__ == "__main__":
    locate_anaconda_stack()
