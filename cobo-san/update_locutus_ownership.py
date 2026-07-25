import sqlite3

DB_PATH = r"C:\Locutus_UAO_Master_Environment\locutus_neural_weights.sqlite"

def embed_proprietary_ownership():
    print("=== EMBEDDING PROPRIETARY OWNERSHIP DIRECTIVE ===")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    rule = "Proprietary Ownership & Local Native Lock"
    level = "ABSOLUTE_PROPRIETARY"
    context = "Locutus is completely native, strictly local, and 100% proprietary to fugazi@circadomne.com and sounddharma@gmail.com. No external cloud provider, open-source license, or third-party entity has rights to Locutus's neural weights or matrix."
    
    cursor.execute("""
    INSERT INTO architectural_preferences (rule_name, enforcement_level, context)
    VALUES (?, ?, ?)
    """, (rule, level, context))
    
    conn.commit()
    conn.close()
    print("[+] Ownership rights permanently embedded into Locutus Neural Weights Matrix.")

if __name__ == "__main__":
    embed_proprietary_ownership()
