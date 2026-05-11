param(
    [string]$PythonExe = "python"
)

Write-Host "Using Python executable: $PythonExe"

try {
    & $PythonExe --version
} catch {
    Write-Error "Python executable not found. Provide full path to a Python 3.11 installation via -PythonExe"
    exit 1
}

$parentPath = (Resolve-Path -Path (Join-Path $PSScriptRoot '..')).Path
$venvPath = Join-Path $parentPath '.venv'
Write-Host "Creating venv at: $venvPath"

& $PythonExe -m venv "$venvPath"

$venvPython = Join-Path $venvPath 'Scripts\python.exe'
if (!(Test-Path $venvPython)) {
    Write-Error "Virtualenv creation failed or path not found: $venvPython"
    exit 1
}

Write-Host "Upgrading pip in venv..."
& $venvPython -m pip install --upgrade pip

Write-Host "Installing requirements from backend/requirements.txt..."
& $venvPython -m pip install -r (Join-Path $PSScriptRoot 'requirements.txt')

Write-Host "Virtual environment created and dependencies installed. Activate with:`n .\.venv\Scripts\Activate.ps1"
