$p = Start-Process 'D:\PROJECTS\CURSORS\CURSOR ENTERPRISE FRAMEWORK GENERATOR\cursor-setup-gui-wpf\bin\publish\VibeCodeEnterpriseFramework.exe' -PassThru
Start-Sleep 5
if ($p.HasExited) { 
    Write-Host "Crashed: $($p.ExitCode)"
} else { 
    Write-Host "App running OK"
    Stop-Process $p -Force 
}
