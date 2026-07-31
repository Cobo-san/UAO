import os
import sqlite3
import datetime

def main():
    repo_dir = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository"
    db_path = os.path.join(repo_dir, "synaptic_matrix", "universal_synaptic_matrix.sqlite")
    
    print("ETL starting for .md and .dat files...")
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS etl_extracted_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path TEXT UNIQUE,
        file_type TEXT,
        file_size INTEGER,
        last_modified TEXT,
        content BLOB
    )
    """)
    
    count = 0
    for root, dirs, files in os.walk(repo_dir):
        if ".git" in root or "synaptic_matrix" in root:
            continue
        for file in files:
            if file.endswith(".md") or file.endswith(".dat"):
                path = os.path.join(root, file)
                ext = ".md" if file.endswith(".md") else ".dat"
                size = os.path.getsize(path)
                mtime = os.path.getmtime(path)
                mtime_str = datetime.datetime.fromtimestamp(mtime).isoformat()
                
                try:
                    with open(path, "rb") as f:
                        content = f.read()
                except Exception as e:
                    print(f"Failed to read {path}: {e}")
                    continue
                
                try:
                    cur.execute("""
                    INSERT OR REPLACE INTO etl_extracted_files (file_path, file_type, file_size, last_modified, content)
                    VALUES (?, ?, ?, ?, ?)
                    """, (path, ext, size, mtime_str, content))
                    count += 1
                except Exception as e:
                    print(f"Failed to insert {path}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"ETL Complete! Processed {count} files and loaded them into universal_synaptic_matrix.sqlite.")

if __name__ == "__main__":
    main()
