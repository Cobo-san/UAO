import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

app = FastAPI(title="Locutus UAO Neural Gateway", version="1.0")

# Secure CORS: Strictly allow local web interface (Zero-Trust)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\synaptic_matrix\locutus_neural_weights.sqlite"

@app.get("/")
def read_root():
    return {"status": "ONLINE", "matrix_size": 14, "identity": "Dual-Identity Cryptographic Protocol Active"}

@app.get("/api/matrix/status")
def get_matrix_status():
    """Returns the live status of the 14-Node Dual-Identity Cloud Matrix."""
    # In a full implementation, this would query the cloud APIs. 
    # For now, it returns the structural blueprint status.
    return {
        "status": "Awaiting Ignition",
        "nodes": 14,
        "identities": ["sounddharma@gmail.com", "fugazi@circadomine.com"],
        "local_mirrors": ["AlmaLinux-10", "Ubuntu"],
        "prime_node_affinity": "E-Cores Active"
    }

@app.get("/api/neural/logs")
def get_neural_logs():
    """Reads the local SQLite Synaptic Matrix."""
    if not os.path.exists(DB_PATH):
        return {"logs": [], "message": "No database found yet."}
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Ensure the table exists before querying
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='action_logs'")
        if not cursor.fetchone():
             return {"logs": [], "message": "Matrix is pristine."}
             
        cursor.execute("SELECT timestamp, action_type, description FROM action_logs ORDER BY id DESC LIMIT 50")
        rows = cursor.fetchall()
        conn.close()
        return {"logs": [{"timestamp": r[0], "type": r[1], "description": r[2]} for r in rows]}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("[+] UAO Neural FastAPI Gateway Initializing...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
