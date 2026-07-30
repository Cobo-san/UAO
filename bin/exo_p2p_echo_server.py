#!/usr/bin/env python3
"""
Exo P2P Echo & Telemetry Server
1. Listens for P2P mesh ping/echo requests on TCP/UDP port 50050 and HTTP port 8082.
2. Returns a 32-byte binary echo header with magic 0x41494756 v2.
3. Registers the route 'mcp_route_exo_echo_server' in universal_synaptic_matrix.sqlite.
4. Executes verification test showing 'ECHO TEST 100% OK' and invokes save_memories_and_create_backups.py.
"""

import os
import sys
import time
import struct
import socket
import sqlite3
import threading
import subprocess
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

MAGIC = 0x41494756  # 0x41494756 = 'AIGV'
VERSION = 2
P2P_PORT = 50050
HTTP_PORT = 8082

REPO_DIR = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository"
DB_PATH = os.path.join(REPO_DIR, "synaptic_matrix", "universal_synaptic_matrix.sqlite")
GDRIVE_DB = r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\Parallel_Synaptic_Database_Matrix\universal_synaptic_matrix.sqlite"

def create_echo_header(total_agents=6, total_storages=5, payload_str=b"EXO_P2P_ECHO"):
    """
    Packs a 32-byte binary IPC/Echo header struct.
    Format: <IHHId12s
    - Magic: 4 bytes unsigned int (0x41494756)
    - Version: 2 bytes unsigned short (2)
    - Total Agents: 2 bytes unsigned short
    - Total Storages: 4 bytes unsigned int
    - Timestamp: 8 bytes double
    - Reserved/Payload: 12 bytes
    Total: 4 + 2 + 2 + 4 + 8 + 12 = 32 bytes
    """
    ts = time.time()
    if len(payload_str) < 12:
        payload_str = payload_str.ljust(12, b"\x00")
    else:
        payload_str = payload_str[:12]
    return struct.pack("<IHHId12s", MAGIC, VERSION, total_agents, total_storages, ts, payload_str)

def unpack_echo_header(data):
    if len(data) != 32:
        raise ValueError(f"Header size must be 32 bytes, got {len(data)} bytes")
    magic, version, agents, storages, ts, reserved = struct.unpack("<IHHId12s", data)
    return {
        "magic": hex(magic),
        "magic_int": magic,
        "version": version,
        "total_agents": agents,
        "total_storages": storages,
        "timestamp": ts,
        "reserved": reserved
    }

def register_mcp_route():
    """Registers 'mcp_route_exo_echo_server' in SQLite WAL Database."""
    dbs = [DB_PATH, GDRIVE_DB]
    for db in dbs:
        db_dir = os.path.dirname(db)
        if not os.path.exists(db_dir):
            continue
        try:
            if os.path.exists(db):
                try:
                    os.chmod(db, 0o666)
                except Exception:
                    pass
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS mcp_synaptic_routes (
                route_id TEXT PRIMARY KEY,
                source_distro TEXT,
                route_type TEXT,
                target_destination TEXT,
                mcp_port INTEGER,
                latency_ms REAL,
                status TEXT
            );
            """)
            cur.execute("""
            INSERT OR REPLACE INTO mcp_synaptic_routes
            VALUES ('mcp_route_exo_echo_server', 'Host', 'EXO_P2P_ECHO', 'P2P_MESH_TELEMETRY', 50050, 0.05, 'ACTIVE_LISTENING');
            """)
            conn.commit()
            conn.close()
            print(f"[+] Registered 'mcp_route_exo_echo_server' in: {db}")
        except Exception as e:
            print(f"[!] Warning registering route in {db}: {e}")

class ExoHTTPRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Quiet logger

    def do_GET(self):
        header = create_echo_header(payload_str=b"HTTP_ECHO_P2P")
        self.send_response(200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("X-Exo-Magic", "0x41494756")
        self.send_header("X-Exo-Version", "2")
        self.send_header("Content-Length", str(len(header)))
        self.end_headers()
        self.wfile.write(header)

    def do_POST(self):
        self.do_GET()

def start_tcp_p2p_listener(stop_event):
    """Listens for TCP P2P mesh ping/echo requests on port 50050."""
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("0.0.0.0", P2P_PORT))
    server_sock.listen(128)
    server_sock.settimeout(0.5)

    while not stop_event.is_set():
        try:
            client, addr = server_sock.accept()
            with client:
                data = client.recv(1024)
                response = create_echo_header(payload_str=b"TCP_ECHO_P2P")
                client.sendall(response)
        except socket.timeout:
            continue
        except Exception:
            break
    server_sock.close()

def start_udp_p2p_listener(stop_event):
    """Listens for UDP P2P mesh ping/echo requests on port 50050."""
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.bind(("0.0.0.0", P2P_PORT))
    udp_sock.settimeout(0.5)

    while not stop_event.is_set():
        try:
            data, addr = udp_sock.recvfrom(1024)
            response = create_echo_header(payload_str=b"UDP_ECHO_P2P")
            udp_sock.sendto(response, addr)
        except socket.timeout:
            continue
        except Exception:
            break
    udp_sock.close()

def start_http_listener(stop_event):
    """Listens for HTTP ping/echo requests on port 8082."""
    httpd = HTTPServer(("0.0.0.0", HTTP_PORT), ExoHTTPRequestHandler)
    httpd.timeout = 0.5
    while not stop_event.is_set():
        httpd.handle_request()
    httpd.server_close()

def verify_exo_echo_server():
    """Performs quick verification test of P2P TCP, UDP, HTTP, and DB route registration."""
    print("==========================================================================")
    print("      EXO P2P ECHO & TELEMETRY SERVER QUICK VERIFICATION TEST             ")
    print("==========================================================================")
    
    # 1. Test TCP 50050
    tcp_ok = False
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(("127.0.0.1", P2P_PORT))
        s.sendall(b"PING_TCP")
        data = s.recv(1024)
        s.close()
        parsed = unpack_echo_header(data)
        if parsed["magic_int"] == MAGIC and parsed["version"] == VERSION and len(data) == 32:
            tcp_ok = True
            print(f"  [+] TCP Port 50050 Echo: PASSED (Header Size: {len(data)}B | Magic: {parsed['magic']} | Version: {parsed['version']})")
    except Exception as e:
        print(f"  [-] TCP Port 50050 Echo Error: {e}")

    # 2. Test UDP 50050
    udp_ok = False
    try:
        u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        u.settimeout(2.0)
        u.sendto(b"PING_UDP", ("127.0.0.1", P2P_PORT))
        data, _ = u.recvfrom(1024)
        u.close()
        parsed = unpack_echo_header(data)
        if parsed["magic_int"] == MAGIC and parsed["version"] == VERSION and len(data) == 32:
            udp_ok = True
            print(f"  [+] UDP Port 50050 Echo: PASSED (Header Size: {len(data)}B | Magic: {parsed['magic']} | Version: {parsed['version']})")
    except Exception as e:
        print(f"  [-] UDP Port 50050 Echo Error: {e}")

    # 3. Test HTTP 8082
    http_ok = False
    try:
        req = urllib.request.urlopen(f"http://127.0.0.1:{HTTP_PORT}/ping", timeout=2.0)
        data = req.read()
        parsed = unpack_echo_header(data)
        if req.status == 200 and parsed["magic_int"] == MAGIC and parsed["version"] == VERSION and len(data) == 32:
            http_ok = True
            print(f"  [+] HTTP Port 8082 Echo: PASSED (Header Size: {len(data)}B | Magic: {parsed['magic']} | Version: {parsed['version']})")
    except Exception as e:
        print(f"  [-] HTTP Port 8082 Echo Error: {e}")

    # 4. Check SQLite Route Registration
    db_ok = False
    try:
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            row = cur.execute("SELECT * FROM mcp_synaptic_routes WHERE route_id='mcp_route_exo_echo_server'").fetchone()
            conn.close()
            if row:
                db_ok = True
                print(f"  [+] SQLite Route Registration: PASSED ({row[0]} -> {row[3]}:{row[4]})")
    except Exception as e:
        print(f"  [-] SQLite Route Check Error: {e}")

    if tcp_ok and udp_ok and http_ok and db_ok:
        print("\n==========================================================================")
        print("                         ECHO TEST 100% OK                                ")
        print("==========================================================================")
        return True
    else:
        print("\n[!] VERIFICATION FAILED!")
        return False

def save_memories():
    """Invokes save_memories_and_create_backups.py script."""
    script_path = os.path.join(REPO_DIR, "bin", "save_memories_and_create_backups.py")
    if os.path.exists(script_path):
        print("\n[*] Invoking Memory Preservation & Backup Engine...")
        try:
            subprocess.check_call([sys.executable, script_path])
            print("[+] Memory preservation and backup synchronization completed successfully.")
        except Exception as e:
            print(f"[!] Error running save_memories_and_create_backups.py: {e}")
    else:
        print(f"[!] Backup script not found at {script_path}")

def main():
    print("==========================================================================")
    print("         EXO P2P ECHO & TELEMETRY SERVER (MAGIC 0x41494756 v2)            ")
    print("==========================================================================")
    
    # 1. Register Route in SQLite WAL Matrix
    register_mcp_route()

    # 2. Start Listeners in Background Threads
    stop_event = threading.Event()
    
    tcp_thread = threading.Thread(target=start_tcp_p2p_listener, args=(stop_event,), daemon=True)
    udp_thread = threading.Thread(target=start_udp_p2p_listener, args=(stop_event,), daemon=True)
    http_thread = threading.Thread(target=start_http_listener, args=(stop_event,), daemon=True)

    tcp_thread.start()
    udp_thread.start()
    http_thread.start()

    print(f"  [+] P2P Socket Listener running on TCP/UDP Port {P2P_PORT}")
    print(f"  [+] HTTP Telemetry Listener running on Port {HTTP_PORT}")
    time.sleep(0.5)

    # 3. Run Verification Test
    success = verify_exo_echo_server()

    # 4. Save Memories and Create Backups if verified
    if success:
        save_memories()

    # If run in interactive daemon mode or command line, keep listeners alive or return success
    if "--daemon" in sys.argv:
        print("[*] Server running in daemon mode. Press Ctrl+C to terminate.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            stop_event.set()
            print("[*] Shutting down Exo P2P Echo Server.")

if __name__ == "__main__":
    main()
