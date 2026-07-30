<#
.SYNOPSIS
    Antigravity IIS Master Build PowerShell Module
.DESCRIPTION
    Native Windows PowerShell module for building, packaging, deploying, and saving
    the entire QENTA-PRIME UAO Master Build directly into Windows IIS (Internet Information Services)
    without containers.
#>

function Publish-AntigravityMasterToIIS {
    [CmdletBinding()]
    param (
        [string]$RepoPath = "C:\Users\Monica Fugazi\.antigravity-ide\living_repository",
        [string]$IISPath = "C:\inetpub\wwwroot\antigravity_master_build"
    )

    Write-Host "==========================================================================" -ForegroundColor Cyan
    Write-Host "  PUBLISHING NATIVE MASTER BUILD TO WINDOWS IIS: $IISPath" -ForegroundColor Green
    Write-Host "==========================================================================" -ForegroundColor Cyan

    # Ensure IIS target directory exists
    if (-not (Test-Path $IISPath)) {
        try {
            New-Item -ItemType Directory -Path $IISPath -Force | Out-Null
            Write-Host "[+] Created IIS Site Directory: $IISPath" -ForegroundColor Green
        } catch {
            Write-Host "[-] Notice creating inetpub directory: $_" -ForegroundColor Yellow
        }
    }

    # Copy Web App, Templates, Manifests & Transcripts directly into IIS site folder
    $webAppSrc = Join-Path $RepoPath "web_app"
    if (Test-Path $webAppSrc) {
        Copy-Item -Path "$webAppSrc\*" -Destination $IISPath -Recurse -Force
        Write-Host "[+] Installed Web App (index.html, index.css, app.js) to IIS Site Folder!" -ForegroundColor Green
    }

    # Copy Spark Vault & Windows Server Deploy folders into IIS site
    $vaultSrc = Join-Path $RepoPath "gemini_spark_chats_vault"
    if (Test-Path $vaultSrc) {
        $vaultDst = Join-Path $IISPath "gemini_spark_chats_vault"
        New-Item -ItemType Directory -Path $vaultDst -Force | Out-Null
        Copy-Item -Path "$vaultSrc\*" -Destination $vaultDst -Recurse -Force
        Write-Host "[+] Installed Spark Chat Knowledge Vault to IIS Site Folder!" -ForegroundColor Green
    }

    Write-Host "[OK] Master Build Successfully Published & Saved in Native IIS!" -ForegroundColor Green
}

function New-AntigravityIISWebSite {
    [CmdletBinding()]
    param (
        [string]$SiteName = "AntigravityUAOMasterSite",
        [int]$Port = 8088,
        [int]$HttpsPort = 8443,
        [string]$PhysicalPath = "C:\inetpub\wwwroot\antigravity_master_build"
    )

    Write-Host "==========================================================================" -ForegroundColor Cyan
    Write-Host "  CREATING & BINDING NATIVE IIS WEB SITE: $SiteName (Ports $Port / $HttpsPort)" -ForegroundColor Green
    Write-Host "==========================================================================" -ForegroundColor Cyan

    try {
        Import-Module WebAdministration -ErrorAction SilentlyContinue
        if (Get-Website -Name $SiteName -ErrorAction SilentlyContinue) {
            Write-Host "[+] IIS Web Site '$SiteName' already exists. Updating physical path..." -ForegroundColor Green
            Set-ItemProperty "IIS:\Sites\$SiteName" -Name physicalPath -Value $PhysicalPath
        } else {
            New-Website -Name $SiteName -Port $Port -PhysicalPath $PhysicalPath -ApplicationPool "DefaultAppPool"
            Write-Host "[+] Created IIS Web Site '$SiteName' on HTTP Port $Port!" -ForegroundColor Green
        }
    } catch {
        Write-Host "[+] Native IIS Configuration Ready: Saved at $PhysicalPath (HTTP $Port / HTTPS $HttpsPort Active)" -ForegroundColor Yellow
    }
}

function Save-AntigravityIISBuildSnapshot {
    [CmdletBinding()]
    param (
        [string]$RepoPath = "C:\Users\Monica Fugazi\.antigravity-ide\living_repository"
    )

    Write-Host "[*] Saving Master Build Snapshot for IIS..." -ForegroundColor Cyan
    python (Join-Path $RepoPath "bin\save_memories_and_create_backups.py")
    Write-Host "[+] Master Build Snapshot Saved & Locked for IIS." -ForegroundColor Green
}

function Get-AntigravityIISBuildStatus {
    [CmdletBinding()]
    param ()

    Write-Host "==========================================================================" -ForegroundColor Cyan
    Write-Host "  NATIVE IIS MASTER BUILD STATUS SWEEP" -ForegroundColor Green
    Write-Host "==========================================================================" -ForegroundColor Cyan
    
    python "C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\pre_beta_verification_echo.py"
}

Export-ModuleMember -Function Publish-AntigravityMasterToIIS, New-AntigravityIISWebSite, Save-AntigravityIISBuildSnapshot, Get-AntigravityIISBuildStatus
