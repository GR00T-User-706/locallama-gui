$ErrorActionPreference = 'Stop'

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$DistRoot = Join-Path $RepoRoot 'dist'
$PyInstaller = Join-Path $RepoRoot '.venv\Scripts\pyinstaller.exe'

if (-not (Test-Path $PyInstaller)) {
    $PyInstaller = 'pyinstaller'
}

Push-Location $RepoRoot
try {
    & $PyInstaller --noconfirm --clean --distpath $DistRoot --workpath (Join-Path $RepoRoot 'build\pyinstaller') (Join-Path $RepoRoot 'packaging\pyinstaller\myloai.spec')
    if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed with exit code $LASTEXITCODE" }

    $Bundle = Join-Path $DistRoot 'MyLoAI Control Center'
    if (-not (Test-Path $Bundle)) { throw "PyInstaller output not found: $Bundle" }

    $Iscc = Get-Command iscc -ErrorAction SilentlyContinue
    if (-not $Iscc) {
        $DefaultIscc = Join-Path ${env:ProgramFiles(x86)} 'Inno Setup 6\ISCC.exe'
        if (Test-Path $DefaultIscc) { $Iscc = $DefaultIscc }
    }
    if (-not $Iscc) { throw 'Inno Setup 6 (ISCC.exe) is required to create the Windows installer.' }

    & $Iscc.Source (Join-Path $RepoRoot 'packaging\windows\MyLoAI.iss')
    if ($LASTEXITCODE -ne 0) { throw "Inno Setup failed with exit code $LASTEXITCODE" }

    Write-Host "Windows installer created under $DistRoot\installer"
}
finally {
    Pop-Location
}
