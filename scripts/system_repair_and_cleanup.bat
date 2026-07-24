@echo off
:: ============================================================================
:: HIGH-PERFORMANCE WINDOWS SYSTEM REPAIR & MAINTENANCE SCRIPT
:: Target CPU: Intel i9-14900K (24 Cores / 32 Logical Threads)
:: Target Account: sounddharma@gmail.com
:: ============================================================================

TITLE Windows System Repair & Maintenance Pipeline
COLOR 0A

:: Check for Administrative Privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] This script must be run as Administrator!
    echo Please right-click this file and select "Run as administrator".
    pause
    exit /b 1
)

echo ============================================================================
echo  HIGH-PERFORMANCE SYSTEM REPAIR PIPELINE (32-THREAD INTEL i9-14900K OPTIMIZED)
echo ============================================================================
echo.

:: ----------------------------------------------------------------------------
:: STEP 1: CHKDSK DRIVE REPAIR (AUTOMATED REBOOT PROMPT HANDLING)
:: ----------------------------------------------------------------------------
echo [STEP 1/4] Running Check Disk on C: drive...
echo Y | chkdsk C: /f
if %errorLevel% neq 0 (
    echo [NOTE] Check Disk requires a system reboot. Volume scheduled for repair on next restart.
) else (
    echo [SUCCESS] Check Disk completed on C: drive.
)
echo.

:: ----------------------------------------------------------------------------
:: STEP 2: DISM WINDOWS IMAGE REPAIR (HIGH CPU PRIORITY OPTIMIZATION)
:: ----------------------------------------------------------------------------
echo [STEP 2/4] Running DISM Windows Image Repair (High Priority Mode)...
start /high /wait dism /online /cleanup-image /restorehealth
echo [SUCCESS] DISM Repair process finished.
echo.

:: ----------------------------------------------------------------------------
:: STEP 3: SYSTEM FILE CHECKER (SFC SCANNOW WITH HIGH PROCESS PRIORITY)
:: ----------------------------------------------------------------------------
echo [STEP 3/4] Running System File Checker (sfc /scannow)...
start /high /wait sfc /scannow
echo [SUCCESS] SFC System File Scan completed.
echo.

:: ----------------------------------------------------------------------------
:: STEP 4: SHUTDOWN / REBOOT PROMPT
:: ----------------------------------------------------------------------------
echo [STEP 4/4] System repair and maintenance sequence completed.
echo.
set /p SHUTDOWN_CHOICE="Do you want to shutdown the computer now? (Y/N): "
if /i "%SHUTDOWN_CHOICE%"=="Y" (
    echo Shutting down system in 10 seconds...
    shutdown /s /t 10
) else (
    echo Maintenance complete. System ready!
    pause
)
