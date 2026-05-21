
Add-Type -AssemblyName System.Windows.Forms
$wshell = New-Object -ComObject WScript.Shell
$proc = Get-Process "Amazon Quick" -ErrorAction SilentlyContinue

if ($proc) {
    # Bring the window to front using the window title
    $wshell.AppActivate("Amazon Quick")
    Start-Sleep -Seconds 2
    
    # Tentativa de abrir as configuracoes e navegar
    # Geralmente aplicativos baseados em Electron/Web usam Ctrl+, para settings
    $wshell.SendKeys('^{,}') 
    Start-Sleep -Seconds 1
    
    Write-Output "Janela focalizada e comando Ctrl+, enviado."
} else {
    Write-Error "Aplicativo Amazon Quick nao encontrado."
}
