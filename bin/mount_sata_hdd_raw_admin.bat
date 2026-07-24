@echo off
echo =========================================================================
echo  MOUNTING OFFLINE SATA HDD (PHYSICALDRIVE0) INTO LINUX WSL2
echo =========================================================================
powershell -Command "Start-Process powershell -ArgumentList '-NoExit -Command wsl --mount \\.\PHYSICALDRIVE0 --bare' -Verb RunAs"
