@{
    RootModule = 'AntigravityIISMasterBuild.psm1'
    ModuleVersion = '1.0.0'
    GUID = 'b2c3d4e5-f6a7-8901-bcde-2345678901bc'
    Author = 'QENTA-PRIME UAO'
    CompanyName = 'Antigravity AI'
    Copyright = '(c) 2026 Antigravity. All rights reserved.'
    Description = 'Native Windows PowerShell Module for Building, Packaging, and Saving the Master Build directly in Windows IIS'
    PowerShellVersion = '5.1'
    FunctionsToExport = @('Publish-AntigravityMasterToIIS', 'New-AntigravityIISWebSite', 'Save-AntigravityIISBuildSnapshot', 'Get-AntigravityIISBuildStatus')
    CmdletsToExport = @()
    VariablesToExport = '*'
    AliasesToExport = @()
}
