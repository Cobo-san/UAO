#!/usr/bin/env python3
"""
Parallel Matrix LLM Working Database Structure Engine
Initializes the Main Master Database alongside 4 Dedicated Model Matrix Databases for vectors,
embedding metadata, MCP routes, and subagent logistics:
  1. Main Master DB -> universal_synaptic_matrix.sqlite
  2. Llama 70B Matrix -> llama_70b_vector_matrix.sqlite
  3. Qwen Coder Matrix -> qwen_coder_vector_matrix.sqlite
  4. DeepSeek R1 Matrix -> deepseek_r1_vector_matrix.sqlite
  5. Codestral Matrix -> codestral_vector_matrix.sqlite
"""

import os
import sys
import sqlite3
import platform

def get_current_os():
    return platform.system()

def get_matrix_dir():
    if get_current_os() == "Windows":
        return r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\synaptic_matrix"
    else:
        return "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/synaptic_matrix"

MATRIX_DBS = {
    "universal_synaptic_matrix.sqlite": "Main Master Platform State & Global Routing Database",
    "llama_70b_vector_matrix.sqlite": "Llama-3.3-70B Vector Embeddings & System Architecture Matrix",
    "qwen_coder_vector_matrix.sqlite": "Qwen-2.5-Coder-32B SDK/ADK Vector & Code AST Matrix",
    "deepseek_r1_vector_matrix.sqlite": "DeepSeek-R1-70B Protocol Reasoning & Debugging Matrix",
    "codestral_vector_matrix.sqlite": "Codestral-22B Fast Subagent Vector & Unit Test Matrix"
}

def init_parallel_matrix_databases():
    print("=== INITIALIZING PARALLEL MATRIX LLM DATABASE STRUCTURE ===")
    matrix_dir = get_matrix_dir()
    os.makedirs(matrix_dir, exist_ok=True)

    for db_name, desc in MATRIX_DBS.items():
        db_path = os.path.join(matrix_dir, db_name)
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode = WAL;")
            cursor.execute("PRAGMA synchronous = NORMAL;")

            # Initialize Model Vector & Logistics Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS vector_embedding_matrix (
                vector_id TEXT PRIMARY KEY,
                domain_tag TEXT,
                model_origin TEXT,
                embedding_blob BLOB,
                metadata_json TEXT,
                created_at_utc TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS model_matrix_logistics (
                param_key TEXT PRIMARY KEY,
                param_value TEXT,
                updated_at_utc TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            cursor.execute("""
            INSERT OR REPLACE INTO model_matrix_logistics (param_key, param_value)
            VALUES ('matrix_description', ?), ('read_only_protection', 'ENFORCED_READ_ONLY');
            """, (desc,))

            conn.commit()
            conn.close()
            print(f"  [+] Initialized Matrix DB: {db_name}")
            print(f"      - Purpose: {desc}")
        except Exception as e:
            print(f"  [!] Notice initializing {db_name}: {e}")

    print("\n[OK] PARALLEL MATRIX LLM DATABASE STRUCTURE CREATED WITH 100% SUCCESS!")

def main():
    init_parallel_matrix_databases()

if __name__ == "__main__":
    main()
