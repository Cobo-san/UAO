#!/usr/bin/env python3
import os
import json

base_dir = r"C:\AI_Dedicated_Storage_1TB\Cloned_Enterprise_VServers"
print("==========================================================================")
print("     CLONED ENTERPRISE VSERVERS DIRECTORY CONTENTS & MANIFESTS            ")
print("==========================================================================")
print("Directory:", base_dir)

if os.path.exists(base_dir):
    subdirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    print(f"Total Cloned VServer Packages: {len(subdirs)}\n")
    for d in subdirs:
        v_path = os.path.join(base_dir, d)
        manifest_p = os.path.join(v_path, "vserver_manifest.json")
        print(f"• {d}:")
        if os.path.exists(manifest_p):
            with open(manifest_p, "r") as f:
                data = json.load(f)
            name = data.get("name")
            distro = data.get("distro")
            cores = data.get("cpu_cores")
            ram = data.get("ram_gb")
            disk = data.get("disk_gb")
            compiler = data.get("compiler")
            status = data.get("status")
            print(f"   - Name    : {name}")
            print(f"   - Distro  : {distro}")
            print(f"   - Spec    : {cores} Cores | {ram}GB RAM | {disk}GB Disk")
            print(f"   - Compiler: {compiler}")
            print(f"   - Status  : {status}\n")

print("==========================================================================")
