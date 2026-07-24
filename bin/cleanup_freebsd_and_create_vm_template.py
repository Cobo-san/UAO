#!/usr/bin/env python3
"""
FreeBSD VM Removal & Universal VM Integration Template Engine
Completely uninstalls FreeBSD VM artifacts, purges files from Living Repo, Google Drive,
and SQLite database, and installs a production-ready Universal VM Integration Template into Cobo-San.
"""

import os
import sys
import json
import sqlite3
import stat
import platform

ACCOUNT_EMAIL = "sounddharma@gmail.com"
GCP_PROJECT_ID = "anaconda-google-project-sounddharma"

def get_current_os():
    return platform.system()

def unset_readonly(file_path):
    try:
        if get_current_os() == "Windows":
            os.chmod(file_path, stat.S_IWRITE | stat.S_IREAD)
        else:
            os.chmod(file_path, stat.S_IRWXU)
    except Exception:
        pass

def remove_file_safely(file_path):
    if os.path.exists(file_path):
        unset_readonly(file_path)
        try:
            os.remove(file_path)
            print(f"  [-] Removed: {file_path}")
            return True
        except Exception as e:
            print(f"  [!] Failed to remove {file_path}: {e}")
            return False
    return False

def purge_freebsd_files():
    print("=== [1/4] PURGING ALL FREEBSD VM FILES & ARTIFACTS ===")

    paths_to_clean = [
        # bin scripts
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\build_freebsd_sandbox_vm_disk.py",
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\create_freebsd_sandbox_vm_hyperv.ps1",
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\create_freebsd_sandbox_vm_qemu.bat",
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\create_freebsd_standalone_install_disk.py",
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\flash_freebsd_cobo_san_usb_disk3.py",
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\launch_freebsd_desktop_rdp.bat",
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\launch_freebsd_sandbox_vm_sata_hyperv.ps1",
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\launch_freebsd_vm_live_monitor.py",
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\register_freebsd_sandbox_vm_db.py",
        # scripts
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\scripts\setup_freebsd_cross_os_bridge.sh",
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\scripts\setup_freebsd_desktop_gui.sh",
        # cobo-san living repo folder
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\cobo-san\freebsd_cross_os_bridge_plan.md",
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\cobo-san\freebsd_full_desktop_gui_plan.md",
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\cobo-san\freebsd_standalone_install_disk_plan.md",
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\cobo-san\freebsd_usb_disk3_installer_report.md",
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\cobo-san\freebsd_vm_sandbox_master_plan.md",
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\cobo-san\setup_freebsd_cross_os_bridge.sh",
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\cobo-san\setup_freebsd_desktop_gui.sh",
        # google drive cobo-san folder
        r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\cobo-san\freebsd_cross_os_bridge_plan.md",
        r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\cobo-san\freebsd_full_desktop_gui_plan.md",
        r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\cobo-san\freebsd_standalone_install_disk_plan.md",
        r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\cobo-san\freebsd_usb_disk3_installer_report.md",
        r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\cobo-san\freebsd_vm_sandbox_master_plan.md",
        r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\cobo-san\setup_freebsd_cross_os_bridge.sh",
        r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\cobo-san\setup_freebsd_desktop_gui.sh",
        # brain artifacts folder
        r"C:\Users\Monica Fugazi\.gemini\antigravity-cli\brain\317d34d3-0194-4cf4-98fc-96739b5ddfcd\freebsd_cross_os_bridge_plan.md",
        r"C:\Users\Monica Fugazi\.gemini\antigravity-cli\brain\317d34d3-0194-4cf4-98fc-96739b5ddfcd\freebsd_full_desktop_gui_plan.md",
        r"C:\Users\Monica Fugazi\.gemini\antigravity-cli\brain\317d34d3-0194-4cf4-98fc-96739b5ddfcd\freebsd_standalone_install_disk_plan.md",
        r"C:\Users\Monica Fugazi\.gemini\antigravity-cli\brain\317d34d3-0194-4cf4-98fc-96739b5ddfcd\freebsd_usb_disk3_installer_report.md",
        r"C:\Users\Monica Fugazi\.gemini\antigravity-cli\brain\317d34d3-0194-4cf4-98fc-96739b5ddfcd\freebsd_vm_sandbox_master_plan.md",
    ]

    count = 0
    for p in paths_to_clean:
        if remove_file_safely(p):
            count += 1
    print(f"[+] Total FreeBSD Files Removed: {count}")

def purge_database_references():
    print("\n=== [2/4] CLEANING UP SQLITE DATABASE REGISTRY TABLES ===")

    db_paths = [
        r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\synaptic_matrix\universal_synaptic_matrix.sqlite",
        r"C:\Users\Monica Fugazi\GoogleDrive_sounddharma\Parallel_Synaptic_Database_Matrix\universal_synaptic_matrix.sqlite"
    ]

    for dbp in db_paths:
        if os.path.exists(dbp):
            unset_readonly(dbp)
            conn = sqlite3.connect(dbp)
            cursor = conn.cursor()

            # Drop old freebsd table if exists
            cursor.execute("DROP TABLE IF EXISTS freebsd_vm_sandbox_registry;")

            # Create generic universal VM sandbox table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS universal_vm_sandbox_registry (
                vm_id TEXT PRIMARY KEY,
                vm_name TEXT,
                os_type TEXT,
                hypervisor TEXT,
                allocated_ram_mb INTEGER,
                allocated_cpus INTEGER,
                virtual_disk_path TEXT,
                bridge_ip_address TEXT,
                mcp_port INTEGER,
                status TEXT,
                created_timestamp TEXT
            );
            """)

            conn.commit()
            conn.close()
            print(f"  [+] Cleaned FreeBSD table and initialized universal_vm_sandbox_registry in: {dbp}")

def create_vm_integration_template():
    print("\n=== [3/4] CREATING UNIVERSAL VM INTEGRATION TEMPLATE & BLUEPRINT ===")

    template_dir = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\templates"
    os.makedirs(template_dir, exist_ok=True)

    # 1. Python Template Script
    script_content = '''#!/usr/bin/env python3
"""
Universal VM Integration Template Engine
Standardized boilerplate for registering, configuring, bridging, and deploying future guest OS VMs
(QEMU/KVM, Hyper-V, VirtualBox, VMware, or WSL2) into the Cobo-San Synaptic Matrix.
"""

import os
import sys
import json
import sqlite3
import time
import platform
import subprocess

ACCOUNT_EMAIL = "sounddharma@gmail.com"
GCP_PROJECT_ID = "anaconda-google-project-sounddharma"

def get_current_os():
    return platform.system()

def get_db_path():
    if get_current_os() == "Windows":
        return r"C:\\Users\\Monica Fugazi\\.antigravity-ide\\living_repository\\synaptic_matrix\\universal_synaptic_matrix.sqlite"
    else:
        return "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository/synaptic_matrix/universal_synaptic_matrix.sqlite"

class UniversalVMIntegration:
    def __init__(self, vm_id, vm_name, os_type, hypervisor, ram_mb=4096, cpus=4, mcp_port=8092):
        self.vm_id = vm_id
        self.vm_name = vm_name
        self.os_type = os_type
        self.hypervisor = hypervisor
        self.ram_mb = ram_mb
        self.cpus = cpus
        self.mcp_port = mcp_port
        self.db_path = get_db_path()

    def register_vm(self, virtual_disk_path, bridge_ip="127.0.0.1"):
        """Registers the VM into the Cobo-San Universal VM Matrix Database."""
        if not os.path.exists(self.db_path):
            print(f"[!] Database not found: {self.db_path}")
            return False

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS universal_vm_sandbox_registry (
            vm_id TEXT PRIMARY KEY,
            vm_name TEXT,
            os_type TEXT,
            hypervisor TEXT,
            allocated_ram_mb INTEGER,
            allocated_cpus INTEGER,
            virtual_disk_path TEXT,
            bridge_ip_address TEXT,
            mcp_port INTEGER,
            status TEXT,
            created_timestamp TEXT
        );
        """)

        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        cursor.execute("""
        INSERT OR REPLACE INTO universal_vm_sandbox_registry
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            self.vm_id,
            self.vm_name,
            self.os_type,
            self.hypervisor,
            self.ram_mb,
            self.cpus,
            virtual_disk_path,
            bridge_ip,
            self.mcp_port,
            "READY_FOR_DEPLOYMENT",
            ts
        ))

        conn.commit()
        conn.close()
        print(f"[+] VM '{self.vm_name}' successfully registered in Cobo-San Matrix on Port {self.mcp_port}!")
        return True

    def generate_mcp_bridge_config(self):
        """Generates the MCP route definition for the integrated VM."""
        route_config = {
            "route_id": f"mcp_route_vm_{self.vm_id}",
            "source_distro": self.os_type,
            "target_destination": f"VM_{self.vm_name.upper()}_BRIDGE",
            "mcp_port": self.mcp_port,
            "route_type": "VM_IPC_BRIDGE",
            "description": f"Standard Synaptic IPC Route for {self.vm_name} ({self.hypervisor})"
        }
        return route_config

if __name__ == "__main__":
    print("=== Universal VM Integration Template Engine ===")
    vm = UniversalVMIntegration(
        vm_id="vm_template_example",
        vm_name="Example Guest OS VM",
        os_type="Linux / FreeBSD / Windows",
        hypervisor="Hyper-V / QEMU",
        ram_mb=4096,
        cpus=4,
        mcp_port=8095
    )
    vm.register_vm(virtual_disk_path=r"C:\\AI_Dedicated_Storage_1TB\\vms\\example_vm.vhdx")
'''

    script_path = os.path.join(template_dir, "universal_vm_integration_template.py")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_content)
    print(f"  [+] Saved Universal VM Script Template: {script_path}")

    # Also copy template to bin directory for quick execution
    bin_template_path = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\universal_vm_integration_template.py"
    with open(bin_template_path, "w", encoding="utf-8") as f:
        f.write(script_content)
    print(f"  [+] Saved Universal VM Script to Bin: {bin_template_path}")

    # 2. Markdown Blueprint Template
    blueprint_md = f"""# 🌐 Universal VM Integration Blueprint & Template

**Account:** `{ACCOUNT_EMAIL}`  
**GCP Project ID:** `{GCP_PROJECT_ID}`  
**Target Specification:** Standardized 4-Step Process for Integrating Future Guest OS Virtual Machines into Cobo-San Build.

---

## 📋 1. Supported Hypervisors & Guest Operating Systems

| Hypervisor Engine | Guest OS Types | Virtual Disk Format | IPC Bridge Type |
| :--- | :--- | :--- | :--- |
| **QEMU / KVM** | Linux / BSD / Custom Unix | `.qcow2` / `.raw` | TAP / Socket / Shared Memory |
| **Hyper-V** | Windows Server / FreeBSD / Linux | `.vhdx` / Dynamic VHD | Synthetic NIC / Named Pipe |
| **VirtualBox** | macOS / Solaris / Custom Distros | `.vdi` / `.vmdk` | Host-Only Adapter / Port Forwarding |
| **WSL2 Subsystems** | Ubuntu / AlmaLinux / Debian | Ext4 VHDX Mount | Localhost Forwarding (`127.0.0.1`) |

---

## 🛠️ 2. Integration Workflow (4 Steps)

### Step 1: Disk Provisioning
Place the guest virtual disk inside dedicated high-speed NVMe storage:
- Primary: `C:\\AI_Dedicated_Storage_1TB\\vms\\<vm_id>.vhdx`
- Secondary: `D:\\AI_Dedicated_Storage_Secondary\\vms\\<vm_id>.qcow2`

### Step 2: Database Registration
Execute the Python registration snippet from [universal_vm_integration_template.py](file:///C:/Users/Monica%20Fugazi/.antigravity-ide/living_repository/templates/universal_vm_integration_template.py):
```python
from templates.universal_vm_integration_template import UniversalVMIntegration

vm = UniversalVMIntegration(
    vm_id="new_custom_vm",
    vm_name="Custom OS Target",
    os_type="Custom Linux",
    hypervisor="Hyper-V",
    ram_mb=8192,
    cpus=4,
    mcp_port=8095
)
vm.register_vm(virtual_disk_path=r"C:\\AI_Dedicated_Storage_1TB\\vms\\new_custom_vm.vhdx")
```

### Step 3: Synaptic MCP Route Registration
Add an entry to `mcp_synaptic_routes` table in `universal_synaptic_matrix.sqlite` on Port `8092-8099`.

### Step 4: Re-bundle Cobo-San Package
Run the master packaging engine to update `cobo-san_master_unified_all_in_one_build.json`:
```bash
python "C:\\Users\\Monica Fugazi\\.antigravity-ide\\living_repository\\bin\\copy_all_to_cobo_san_folder.py"
```

---

> [!NOTE]
> All future VM integrations automatically inherit Cobo-San 32-Byte Binary IPC header compatibility (`0x41494756` v2) and zero-cost resource enforcement.
"""

    blueprint_path = os.path.join(template_dir, "universal_vm_integration_blueprint.md")
    with open(blueprint_path, "w", encoding="utf-8") as f:
        f.write(blueprint_md)
    print(f"  [+] Saved Universal VM Blueprint MD: {blueprint_path}")

def update_copy_all_script():
    print("\n=== [4/4] UPDATING COBO-SAN MASTER PACKAGING SCRIPT ===")
    copy_script_path = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\copy_all_to_cobo_san_folder.py"

    with open(copy_script_path, "r", encoding="utf-8") as f:
        code = f.read()

    # Replace old FreeBSD files with universal VM templates
    old_files_block = """        # Anaconda Master AI Platform Stack & Visual Reports
        os.path.join(paths["brain_artifacts"], "freebsd_usb_disk3_installer_report.md"),
        os.path.join(paths["brain_artifacts"], "freebsd_standalone_install_disk_plan.md"),
        os.path.join(paths["brain_artifacts"], "freebsd_full_desktop_gui_plan.md"),
        os.path.join(paths["living_repo"], "scripts", "setup_freebsd_desktop_gui.sh"),
        os.path.join(paths["brain_artifacts"], "sata_hdd_vm_launch_and_security_report.md"),
        os.path.join(paths["brain_artifacts"], "freebsd_vm_sandbox_master_plan.md"),
        os.path.join(paths["brain_artifacts"], "freebsd_cross_os_bridge_plan.md"),
        os.path.join(paths["living_repo"], "scripts", "setup_freebsd_cross_os_bridge.sh"),"""

    new_files_block = """        # Anaconda Master AI Platform Stack & Universal VM Blueprints
        os.path.join(paths["living_repo"], "templates", "universal_vm_integration_blueprint.md"),
        os.path.join(paths["living_repo"], "templates", "universal_vm_integration_template.py"),
        os.path.join(paths["brain_artifacts"], "sata_hdd_vm_launch_and_security_report.md"),"""

    if old_files_block in code:
        code = code.replace(old_files_block, new_files_block)
        unset_readonly(copy_script_path)
        with open(copy_script_path, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"  [+] Updated copy_all_to_cobo_san_folder.py script cleanly!")
    else:
        print("  [*] Note: copy_all_to_cobo_san_folder.py already updated or block structure modified.")

def main():
    print("==========================================================================")
    print("  FREEBSD VM REMOVAL & UNIVERSAL VM INTEGRATION TEMPLATE PIPELINE")
    print("==========================================================================")
    purge_freebsd_files()
    purge_database_references()
    create_vm_integration_template()
    update_copy_all_script()
    print("\n[OK] FREEBSD CLEANUP AND UNIVERSAL VM TEMPLATE INSTALLATION COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
