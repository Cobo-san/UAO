@echo off
TITLE Native Cluster-Accelerated System Repair Engine
COLOR 0A

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Must be run as Administrator!
    pause
    exit /b 1
)

powershell -ExecutionPolicy Bypass -File "%~dp0native_cluster_accelerated_repair.ps1"
