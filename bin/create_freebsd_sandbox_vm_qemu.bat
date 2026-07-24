@echo off
echo =========================================================================
echo  PROVISIONING PORTABLE FREEBSD 14.1 SANDBOX VM VIA QEMU / KVM
echo =========================================================================

set "VM_DIR=C:\AI_Dedicated_Storage_1TB\FreeBSD_Sandbox_VM"
if not exist "%VM_DIR%" mkdir "%VM_DIR%"

echo [*] Target Directory: %VM_DIR%
echo [*] Specs: 24 vCPUs, 24 GB RAM, 100 GB VirtIO Storage
echo [*] Command to launch QEMU FreeBSD Sandbox:
echo.
echo qemu-system-x86_64 -name FreeBSD-Sandbox-CoboSan ^
  -m 24G -smp 24,sockets=1,cores=24,threads=1 ^
  -cpu host -enable-kvm ^
  -drive file=C:\AI_Dedicated_Storage_1TB\FreeBSD_Sandbox_VM\freebsd_disk.qcow2,if=virtio,format=qcow2 ^
  -net nic,model=virtio -net user,hostfwd=tcp::2222-:22 ^
  -display default
echo.
pause
