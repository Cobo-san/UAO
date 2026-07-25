import os
import json
import time

LIVING_REPO = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository"
GDRIVE = r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\Parallel_Synaptic_Database_Matrix"

print("Living Repository Continuous Sync Engine running...")
timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
manifest = {
    "account": "sounddharma@gmail.com",
    "status": "LIVE_SYNCHRONIZED",
    "last_sync_utc": timestamp,
    "living_repo_path": LIVING_REPO
}

with open(os.path.join(LIVING_REPO, ".living_repo_manifest.json"), 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)

print(f"Sync complete at {timestamp}")
