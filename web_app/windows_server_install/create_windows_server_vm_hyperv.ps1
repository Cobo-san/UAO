# Hyper-V Automated Windows Server VM Provisioner Script
$VMName = "Windows_Server_2025_Evaluation_Edition_IIS"
$VMPath = "C:\AI_Dedicated_Storage_1TB\vms\Windows_Server_2025_Eval"
$VHDPath = "$VMPath\Windows_Server_2025_Eval.vhdx"
$RAM = 8GB
$CPUs = 4

Write-Host "=== Provisioning Windows Server 2025 Evaluation Edition VM via IIS ==="
New-Item -Path $VMPath -ItemType Directory -Force | Out-Null
New-VHD -Path $VHDPath -SizeBytes 100GB -Dynamic | Out-Null
New-VM -Name $VMName -MemoryStartupBytes $RAM -VHDPath $VHDPath -Path $VMPath | Out-Null
Set-VMProcessor -VMName $VMName -Count $CPUs
Write-Host "[OK] Windows Server 2025 VM Created Successfully in Hyper-V!"
