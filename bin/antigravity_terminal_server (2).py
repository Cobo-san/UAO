#!/usr/bin/env python3
"""
Antigravity Live Terminal Server (Spaceship Cockpit Backend API)
Listens on localhost:9999 to execute REAL commands on Windows PowerShell, AlmaLinux-10 WSL, Ubuntu WSL, and AGY CLI.
"""

import os
import sys
import json
import subprocess
import platform
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 9999

class TerminalApiHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            
            payload = {
                "status": "ONLINE",
                "os": platform.system(),
                "timestamp_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                "nvme_c_speed": "7,000 MB/s",
                "nvme_d_speed": "3,500 MB/s",
                "gcp_regions": {
                    "Windows": "us-east1",
                    "AlmaLinux": "us-central1",
                    "Ubuntu": "us-west1"
                }
            }
            self.wfile.write(json.dumps(payload).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/exec":
            content_len = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_len).decode("utf-8", errors="ignore")
            
            output = ""
            exit_code = 0
            tab = "pwsh"
            cmd = ""

            try:
                data = json.loads(post_body)
                tab = data.get("tab", "pwsh")
                cmd = data.get("command", "").strip()
            except Exception as parse_err:
                cmd = post_body.strip()

            print(f"[*] Executing Terminal Command [{tab}]: {cmd}")

            try:
                if not cmd:
                    output = "No command provided."
                elif tab == "pwsh":
                    res = subprocess.run(["powershell.exe", "-NoProfile", "-Command", cmd], capture_output=True, text=True, check=False)
                    output = res.stdout if res.returncode == 0 else (res.stdout + "\n" + res.stderr)
                    exit_code = res.returncode
                elif tab == "alma":
                    res = subprocess.run(["wsl.exe", "-d", "AlmaLinux-10", "-u", "root", "bash", "-c", cmd], capture_output=True, text=True, check=False)
                    output = res.stdout if res.returncode == 0 else (res.stdout + "\n" + res.stderr)
                    exit_code = res.returncode
                elif tab == "ubuntu":
                    res = subprocess.run(["wsl.exe", "-d", "Ubuntu", "-u", "root", "bash", "-c", cmd], capture_output=True, text=True, check=False)
                    output = res.stdout if res.returncode == 0 else (res.stdout + "\n" + res.stderr)
                    exit_code = res.returncode
                elif tab == "agy":
                    repo_dir = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository"
                    res = subprocess.run([sys.executable, os.path.join(repo_dir, "bin", "verify_system_status.py")], capture_output=True, text=True, check=False)
                    output = res.stdout
                    exit_code = res.returncode

            except Exception as exec_err:
                output = f"Execution error: {exec_err}"
                exit_code = 1

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            
            resp_payload = {
                "status": "SUCCESS" if exit_code == 0 else "ERROR",
                "exit_code": exit_code,
                "output": output
            }
            self.wfile.write(json.dumps(resp_payload).encode("utf-8"))

def main():
    print(f"=== Antigravity Live Terminal Server Running on http://localhost:{PORT} ===")
    httpd = HTTPServer(("localhost", PORT), TerminalApiHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down Terminal Server.")

if __name__ == "__main__":
    main()
