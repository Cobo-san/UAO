@echo off
echo =========================================================================
echo  CONNECTING TO FREEBSD 14.1 FULL DESKTOP VIA WINDOWS REMOTE DESKTOP (RDP)
echo =========================================================================
echo [*] Target Address: localhost:3389 (FreeBSD XRDP Gateway)
echo [*] Launching mstsc.exe Remote Desktop Client...
start mstsc.exe /v:localhost:3389
