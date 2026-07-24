# Automated Elevated Script to Mount Physical Drive 0 into WSL2
Write-Host "Mounting Physical SATA Disk \\.\PHYSICALDRIVE0 into WSL2..." -ForegroundColor Green
wsl --mount \\.\PHYSICALDRIVE0 --bare
Write-Host "Disk Mounted Successfully as Raw Block Device!" -ForegroundColor Cyan
