$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Testar Relatorio Mob2Con.lnk")
$Shortcut.TargetPath = "C:\Users\Donizete Senne\Desktop\Mob2Con-Central\06-MCP-Tools\scripts-amazon-quick\TESTAR_RELATORIO.bat"
$Shortcut.WorkingDirectory = "C:\Users\Donizete Senne\Desktop\Mob2Con-Central\06-MCP-Tools\scripts-amazon-quick"
$Shortcut.Description = "Gera e abre o relatorio semanal Mob2Con"
$Shortcut.Save()
Write-Host "Atalho criado na Area de Trabalho!" -ForegroundColor Green
