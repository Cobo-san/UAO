# 🌐 Oracle Cloud Always Free: FreeBSD Desktop Cloud VM Blueprint

**Account Target:** `sounddharma@gmail.com`  
**GCP & Multi-Cloud Project:** `anaconda-google-project-sounddharma`  
**Cost Target:** `$0.00 / Month (100% Always Free Guaranteed)`  
**Endpoint Access:** Full Desktop GUI via RDP (`mstsc`), VNC, and Web Browser

---

## 🚀 1. Oracle Cloud Always Free Resource Specs

Oracle Cloud Infrastructure (OCI) provides generous **Always Free Tier** resources that perfectly host a FreeBSD Desktop VM:

| Component | Free Allocation | FreeBSD VM Recommended Spec |
| :--- | :--- | :--- |
| **Compute Architecture** | ARM Ampere A1 (`VM.Standard.A1.Flex`) | 2 to 4 OCPUs (ARM64 / aarch64) |
| **Memory (RAM)** | 24 GB RAM total | 8 GB to 16 GB RAM |
| **Boot Disk Storage** | 200 GB Block Storage | 50 GB to 100 GB NVMe-Backed Disk |
| **Bandwidth** | 10 TB / Month Outbound | Unlimited Inbound |
| **Monthly Cost** | **$0.00 FREE** | **$0.00 FREE** |

---

## 🛠️ 2. Step-by-Step FreeBSD Installation on OCI

Because OCI native launch templates default to Oracle Linux / Ubuntu / AlmaLinux, FreeBSD is installed via **Custom Image Upload** or **mfsBSD Memory Disk Swap**.

### Method A: Custom Image Upload (Recommended)
1. Download official FreeBSD 14.1 ARM64 raw image: `FreeBSD-14.1-RELEASE-arm64-aarch64-RAW.raw.xz`
2. Decompress and convert to QCOW2:
   ```bash
   qemu-img convert -f raw -O qcow2 FreeBSD-14.1-RELEASE-arm64-aarch64-RAW.raw freebsd14-oci.qcow2
   ```
3. Upload `freebsd14-oci.qcow2` to Oracle Cloud Object Storage Bucket.
4. Import as **Custom Image** under `OCI Compute -> Custom Images` (Emulation: `paravirtualized`, Operating System: `FreeBSD`).
5. Launch Instance `oracle-freebsd-desktop` using `VM.Standard.A1.Flex` (4 OCPUs, 16GB RAM).

### Method B: `mfsBSD` Disk Overwrite from Linux
1. Launch Always Free Ubuntu ARM VM on OCI.
2. Download `mfsBSD` image into RAM (`/tmp`).
3. Flash `mfsBSD` directly over `/dev/sda` or `/dev/nvme0n1` and reboot:
   ```bash
   dd if=mfsbsd-14.1-arm64.img of=/dev/nvme0n1 bs=1M status=progress && reboot
   ```
4. Log into `mfsBSD` via SSH and run `bsdinstall` to format ZFS/UFS disk.

---

## 🎨 3. Installing Desktop GUI & Remote Endpoint Access

Once FreeBSD 14.1 boots on Oracle Cloud, install XFCE desktop and Remote Desktop Server (`xrdp`):

```bash
# 1. Update Package Repository & Install Desktop Suite
pkg update && pkg upgrade -y
pkg install -y xfce xfce4-goodies xrdp xorg slim

# 2. Enable Services in /etc/rc.conf
sysrc dbus_enable="YES"
sysrc xrdp_enable="YES"
sysrc xrdp_sesman_enable="YES"

# 3. Configure User XFCE Session for RDP
echo "exec startxfce4" > ~/.xsession
chmod +x ~/.xsession

# 4. Start Services
service dbus start
service xrdp start
service xrdp_sesman start
```

---

## 🔐 4. OCI Ingress Security Rule & Endpoint Access

1. Open OCI Ingress Firewall for RDP Port `3389`:
   * **Source CIDR**: `0.0.0.0/0` (or restricted to your public IP)
   * **IP Protocol**: TCP
   * **Destination Port Range**: `3389`
2. Connect from Windows Host using standard Remote Desktop Connection (`mstsc.exe`):
   * **Computer**: `<OCI_INSTANCE_PUBLIC_IP>:3389`
   * **Username**: `freebsd`
   * **Password**: `<YOUR_FREEBSD_PASSWORD>`

---

## 🧩 5. Integration into Cobo-San Matrix

The FreeBSD Cloud VM is automatically indexed in Cobo-San via [universal_vm_integration_template.py](file:///C:/Users/Monica%20Fugazi/.antigravity-ide/living_repository/templates/universal_vm_integration_template.py):

```python
from templates.universal_vm_integration_template import UniversalVMIntegration

cloud_vm = UniversalVMIntegration(
    vm_id="oci_freebsd_desktop",
    vm_name="Oracle Cloud FreeBSD 14.1 Desktop",
    os_type="FreeBSD ARM64",
    hypervisor="Oracle Cloud Always Free (VM.Standard.A1.Flex)",
    ram_mb=16384,
    cpus=4,
    mcp_port=8095
)

cloud_vm.register_vm(
    virtual_disk_path="oci://bucket-sounddharma/freebsd14-oci.qcow2",
    bridge_ip="<OCI_FREEBSD_PUBLIC_IP>"
)
```

---

> [!TIP]
> **Zero-Cost Guarantee**: Running this 4-Core 16GB RAM FreeBSD Desktop VM on Oracle Cloud Always Free incur **$0.00 charges** forever.
