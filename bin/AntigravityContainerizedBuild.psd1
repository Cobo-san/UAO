@{
    RootModule = 'AntigravityContainerizedBuild.psm1'
    ModuleVersion = '1.0.0'
    GUID = 'a1b2c3d4-e5f6-7890-abcd-1234567890ab'
    Author = 'QENTA-PRIME UAO'
    CompanyName = 'Antigravity AI'
    Copyright = '(c) 2026 Antigravity. All rights reserved.'
    Description = 'PowerShell Module for Containerizing and Orchestrating the QENTA-PRIME UAO Master Build'
    PowerShellVersion = '5.1'
    FunctionsToExport = @('Build-AntigravityContainerImage', 'Start-AntigravityContainerStack', 'Stop-AntigravityContainerStack', 'Get-AntigravityContainerStatus')
    CmdletsToExport = @()
    VariablesToExport = '*'
    AliasesToExport = @()
}
