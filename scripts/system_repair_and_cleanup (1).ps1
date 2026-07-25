# ============================================================================
# HIGH-PERFORMANCE WINDOWS SYSTEM REPAIR & MAINTENANCE POWERSHELL SCRIPT
# Target CPU: Intel i9-14900K (24 Physical Cores / 32 Logical Threads)
# Target Account: sounddharma@gmail.com
# ============================================================================

# Ensure Administrator Elevation
$currentPrincipal = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "[ERROR] This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Please restart PowerShell as Administrator." -ForegroundColor Yellow
    Exit
}

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host " HIGH-PERFORMANCE SYSTEM REPAIR PIPELINE (32-THREAD INTEL i9-14900K OPTIMIZED)" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# ----------------------------------------------------------------------------
# STEP 1: CHKDSK DRIVE REPAIR WITH AUTOMATED REBOOT HANDLING
# ----------------------------------------------------------------------------
Write-Host "[STEP 1/4] Running Check Disk on C: drive..." -ForegroundColor Green
$chkdskOutput = "Y" | chkdsk C: /f
Write-Host "[NOTE] Check Disk process initiated. If volume is locked, it is scheduled for reboot." -ForegroundColor Yellow
Write-Host ""

# ----------------------------------------------------------------------------
# STEP 2: DISM WINDOWS IMAGE REPAIR (HIGH PROCESS PRIORITY)
# ----------------------------------------------------------------------------
Write-Host "[STEP 2/4] Running DISM Image Repair with High CPU Priority (Intel i9-14900K)..." -ForegroundColor Green
$dismProc = Start-Process dism.exe -ArgumentList '/online /cleanup-image /restorehealth' -PassThru -NoNewWindow
$dismProc.PriorityClass = [System.Diagnostics.ProcessPriorityClass]::High
$dismProc.WaitForExit()
Write-Host "[SUCCESS] DISM Repair complete (Exit Code: $($dismProc.ExitCode))." -ForegroundColor Green
Write-Host ""

# ----------------------------------------------------------------------------
# STEP 3: SYSTEM FILE CHECKER (SFC SCANNOW WITH HIGH PROCESS PRIORITY)
# ----------------------------------------------------------------------------
Write-Host "[STEP 3/4] Running System File Checker (sfc /scannow) with High CPU Priority..." -ForegroundColor Green
$sfcProc = Start-Process sfc.exe -ArgumentList '/scannow' -PassThru -NoNewWindow
$sfcProc.PriorityClass = [System.Diagnostics.ProcessPriorityClass]::High
$sfcProc.WaitForExit()
Write-Host "[SUCCESS] SFC System File Scan complete (Exit Code: $($sfcProc.ExitCode))." -ForegroundColor Green
Write-Host ""

# ----------------------------------------------------------------------------
# STEP 4: SHUTDOWN / REBOOT PROMPT
# ----------------------------------------------------------------------------
Write-Host "[STEP 4/4] Maintenance sequence complete." -ForegroundColor Cyan
$response = Read-Host "Do you want to shutdown the computer now? (Y/N)"
if ($response -eq "Y" -or $response -eq "y") {
    Write-Host "Shutting down system..." -ForegroundColor Red
    Stop-Computer -Force
} else {
    Write-Host "System repair complete. Ready for operation!" -ForegroundColor Green
}
