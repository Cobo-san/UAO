@echo off
set "ACTION=%~1"
set "OPT=%~2"
set "OPT3=%~3"

if "%ACTION%"=="cleanup" (
    if "%OPT%"=="restart" (
        powershell -ExecutionPolicy Bypass -Command "& 'C:\Users\Monica Fugazi\.antigravity-ide\living_repository\scripts\native_cluster_accelerated_repair.ps1'; Restart-Computer -Force"
    ) else if "%OPT3%"=="restart" (
        powershell -ExecutionPolicy Bypass -Command "& 'C:\Users\Monica Fugazi\.antigravity-ide\living_repository\scripts\native_cluster_accelerated_repair.ps1'; Restart-Computer -Force"
    ) else if "%OPT%"=="&" (
        powershell -ExecutionPolicy Bypass -Command "& 'C:\Users\Monica Fugazi\.antigravity-ide\living_repository\scripts\native_cluster_accelerated_repair.ps1'; Restart-Computer -Force"
    ) else (
        powershell -ExecutionPolicy Bypass -File "C:\Users\Monica Fugazi\.antigravity-ide\living_repository\scripts\native_cluster_accelerated_repair.ps1"
    )
) else if "%ACTION%"=="restart" (
    powershell -ExecutionPolicy Bypass -Command "& 'C:\Users\Monica Fugazi\.antigravity-ide\living_repository\scripts\native_cluster_accelerated_repair.ps1'; Restart-Computer -Force"
) else if "%ACTION%"=="status" (
    python "C:\Users\Monica Fugazi\.gemini\antigravity-cli\brain\22ded982-37bd-4d05-95d6-c38e669110a1\scratch\check_realtime_system_status.py"
) else (
    echo [cobo-san] Available commands:
    echo   cobo-san cleanup           - Runs Native Cluster Repair Engine
    echo   cobo-san cleanup ^& restart - Runs Repair Engine and automatically REBOOTS
    echo   cobo-san restart           - Runs Repair Engine and automatically REBOOTS
    echo   cobo-san status            - Runs Real-Time System Status Audit
)
