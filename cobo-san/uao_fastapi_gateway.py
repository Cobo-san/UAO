import os
import sqlite3
import psutil
from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
import uvicorn
import json

app = FastAPI(title="Locutus UAO Web Gateway")

DB_PATH = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\synaptic_matrix\universal_synaptic_matrix.sqlite"

# --- CONCURRENCY LOCK CHECK ---
def is_agy_running():
    """Strict check to ensure AGY CLI is not running simultaneously with Web UI."""
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            if proc.info['name'] in ['agy.exe', 'agy']:
                return True
            cmd = proc.info.get('cmdline')
            if cmd and 'agy' in ' '.join(cmd).lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

@app.middleware("http")
async def enforce_mutual_exclusion(request, call_next):
    if is_agy_running():
        return json.dumps({"error": "MUTUAL EXCLUSION LOCK: The AGY CLI is currently active. The Locutus Web Interface cannot be utilized at the same time."}), 423
    response = await call_next(request)
    return response

# --- MODELS ---
class PromptPayload(BaseModel):
    message: str
    target_agent: str = "agent_uao_supreme_architect"

# --- ENDPOINTS ---
@app.get("/api/system/health")
def get_health():
    return {"status": "ACTIVE", "lock_status": "SECURE", "agy_running": False}

@app.get("/api/agents/status")
def get_agents():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT agent_id, agent_name, role, status, mcp_port FROM ai_agents_registry")
        agents = cursor.fetchall()
        conn.close()
        return {"agents": agents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/locutus")
def chat_with_locutus(payload: PromptPayload):
    # This endpoint will proxy REST payloads to Port 8100 (Locutus)
    return {"response": f"Locutus acknowledged: {payload.message}", "routed_to": payload.target_agent}

if __name__ == "__main__":
    print("=== Booting Locutus UAO API Gateway ===")
    print("[*] Binding to 0.0.0.0 (Local & Mobile Access)")
    print("[*] Enforcing AGY Mutual Exclusion Lock")
    # Bind to 0.0.0.0 for Mobile Wi-Fi access
    uvicorn.run(app, host="0.0.0.0", port=8000)
