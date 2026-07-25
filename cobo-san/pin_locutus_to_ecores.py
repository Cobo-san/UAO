import os
import sys
import psutil
import sqlite3

DB_PATH = r"C:\Locutus_UAO_Master_Environment\locutus_neural_weights.sqlite"

def pin_to_efficiency_cores():
    print("==========================================================================")
    print("           LOCUTUS UAO: INTEL i9-14900K E-CORE PINNING ENGINE             ")
    print("==========================================================================")
    
    try:
        # Intel i9-14900K has 32 threads (0-15 are P-Cores, 16-31 are E-Cores usually)
        total_cores = psutil.cpu_count(logical=True)
        print(f"[*] Total Logical Cores Detected: {total_cores}")
        
        # We will dynamically calculate the top 50% of cores as E-Cores (common for Intel hybrid)
        e_core_start = total_cores // 2
        e_cores = list(range(e_core_start, total_cores))
        
        # Get current process
        p = psutil.Process(os.getpid())
        
        # Pin the process to E-Cores
        p.cpu_affinity(e_cores)
        print(f"[+] Successfully pinned Locutus process (PID: {p.pid}) to E-Cores: {e_cores}")
        
        # Save this preference natively into Locutus's mind
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO architectural_preferences (rule_name, enforcement_level, context)
        VALUES (?, ?, ?)
        """, ("E-Core CPU Affinity Lock", "ABSOLUTE", f"Locutus background matrix processes must ALWAYS be pinned exclusively to Intel Efficiency Cores ({e_cores}) to preserve P-Cores for heavy LLM inference."))
        conn.commit()
        conn.close()
        
        print("[+] E-Core Affinity Preference permanently embedded into Locutus Neural Weights.")
        print("==========================================================================")
        print("  [OK] LOCUTUS BACKGROUND PROCESSES OPTIMIZED FOR ZERO-IMPACT 24/7 RUN.")
        print("==========================================================================")
        
    except Exception as e:
        print(f"[!] Failed to pin to E-Cores: {e}")

if __name__ == "__main__":
    pin_to_efficiency_cores()
