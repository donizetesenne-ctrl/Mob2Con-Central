# ============================================
# Configurar Memoria Virtual - EXECUTAR COMO ADMIN
# ============================================
# Clique direito neste arquivo > Executar com PowerShell (Admin)

Write-Host "Configurando memoria virtual..." -ForegroundColor Cyan
Write-Host ""

# 1. Desabilitar gerenciamento automatico
$cs = Get-CimInstance Win32_ComputerSystem
Set-CimInstance $cs -Property @{AutomaticManagedPagefile=$false}
Write-Host "[1/3] Gerenciamento automatico DESABILITADO" -ForegroundColor Green

# 2. Remover pagefile do G: (Google Drive)
$gPF = Get-CimInstance Win32_PageFileSetting -Filter "Name='g:\\pagefile.sys'" -ErrorAction SilentlyContinue
if ($gPF) {
    Remove-CimInstance $gPF
    Write-Host "[2/3] G: pagefile REMOVIDO (Google Drive)" -ForegroundColor Green
} else {
    Write-Host "[2/3] G: pagefile ja nao existe" -ForegroundColor Gray
}

# 3. Configurar C: com 48GB fixo
$cPF = Get-CimInstance Win32_PageFileSetting -Filter "Name='c:\\pagefile.sys'" -ErrorAction SilentlyContinue
if ($cPF) {
    Set-CimInstance $cPF -Property @{InitialSize=49152; MaximumSize=49152}
    Write-Host "[3/3] C: pagefile = 48GB (49152 MB)" -ForegroundColor Green
} else {
    New-CimInstance -ClassName Win32_PageFileSetting -Property @{Name="c:\pagefile.sys"; InitialSize=[uint32]49152; MaximumSize=[uint32]49152}
    Write-Host "[3/3] C: pagefile CRIADO = 48GB" -ForegroundColor Green
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  CONCLUIDO! Reinicie o PC para aplicar." -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
pause