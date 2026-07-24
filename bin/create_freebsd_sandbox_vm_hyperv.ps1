# Automated Hyper-V FreeBSD 14.1 Sandbox VM Creation Script
# Provisions a FreeBSD VM matching host hardware (24 vCPUs, 24GB RAM, VirtIO Storage)

$VMName = "FreeBSD-Sandbox-CoboSan"
$VHDPath = "C:\AI_Dedicated_Storage_1TB\FreeBSD_Sandbox_VM\FreeBSD_Sandbox_Disk.vhdx"
$VMPath = "C:\AI_Dedicated_Storage_1TB\FreeBSD_Sandbox_VM"

Write-Host "=== CREATING FREEBSD 14.1 SANDBOX VM ON HYPER-V ===" -ForegroundColor Green

# 1. Create VM Storage Directory
New-Item -ItemType Directory -Force -Path $VMPath | Out-Null

# 2. Create Dynamic VHDX Disk (100 GB)
if (-not (Test-Path $VHDPath)) {
    Write-Host "[*] Creating 100 GB VHDX Hard Disk at $VHDPath..." -ForegroundColor Yellow
    New-VHD -Path $VHDPath -SizeBytes 100GB -Dynamic | Out-Null
}

# 3. Create Hyper-V VM (24 vCPUs, 24 GB RAM)
if (-not (Get-VM -Name $VMName -ErrorAction SilentlyContinue)) {
    Write-Host "[*] Provisioning Virtual Machine '$VMName' (24 vCPUs, 24GB RAM)..." -ForegroundColor Yellow
    New-VM -Name $VMName -MemoryStartupBytes 24GB -VHDPath $VHDPath -Path $VMPath -Generation 2 | Out-Null
    Set-VM -Name $VMName -ProcessorCount 24 -DynamicMemory -MemoryMinimumBytes 8GB -MemoryMaximumBytes 24GB
    Set-VMFirmware -VMName $VMName -EnableSecureBoot Off
    Write-Host "[+] Virtual Machine '$VMName' Created Successfully!" -ForegroundColor Green
} else {
    Write-Host "[+] Virtual Machine '$VMName' Already Exists." -ForegroundColor Cyan
}

Write-Host "=== FREEBSD SANDBOX VM CREATION COMPLETED ===" -ForegroundColor Green
