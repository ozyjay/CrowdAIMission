$ErrorActionPreference = "Stop"

function Import-DotEnv {
    param([string] $Path)
    if (-not (Test-Path $Path)) {
        return
    }

    foreach ($Line in Get-Content $Path) {
        $Trimmed = $Line.Trim()
        if (-not $Trimmed -or $Trimmed.StartsWith("#") -or -not $Trimmed.Contains("=")) {
            continue
        }

        $Parts = $Trimmed.Split("=", 2)
        Set-Item -Path "Env:$($Parts[0].Trim())" -Value $Parts[1].Trim().Trim('"').Trim("'")
    }
}

function Resolve-PythonBin {
    if ($env:PYTHON_BIN) {
        return $env:PYTHON_BIN
    }
    if (Test-Path ".venv/bin/python3") {
        return ".venv/bin/python3"
    }
    if (Test-Path ".venv/Scripts/python.exe") {
        return ".venv/Scripts/python.exe"
    }
    if (Get-Command pyenv -ErrorAction SilentlyContinue) {
        $PyenvPython = (& pyenv which python3 2>$null)
        if ($PyenvPython) {
            return $PyenvPython.Trim()
        }
    }
    return "python3"
}

function Get-LanIp {
    $Ip = (& ipconfig getifaddr en0 2>$null)
    if ($Ip) {
        return $Ip.Trim()
    }

    $Address = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
        Where-Object { $_.IPAddress -ne "127.0.0.1" -and $_.PrefixOrigin -ne "WellKnown" } |
        Select-Object -First 1 -ExpandProperty IPAddress
    return $Address
}

$EnvAppHost = $env:APP_HOST
$EnvAppPort = $env:APP_PORT
$EnvAppReload = $env:APP_RELOAD
$EnvPythonBin = $env:PYTHON_BIN

Import-DotEnv ".env"

if ($EnvAppHost) { $env:APP_HOST = $EnvAppHost }
if ($EnvAppPort) { $env:APP_PORT = $EnvAppPort }
if ($EnvAppReload) { $env:APP_RELOAD = $EnvAppReload }
if ($EnvPythonBin) { $env:PYTHON_BIN = $EnvPythonBin }

if (-not $env:APP_HOST) { $env:APP_HOST = "127.0.0.1" }
if (-not $env:APP_PORT) { $env:APP_PORT = "3200" }
if (-not $env:APP_RELOAD) { $env:APP_RELOAD = "false" }

$PythonBin = Resolve-PythonBin
$LanIp = Get-LanIp

Write-Host "Starting FastAPI app on $($env:APP_HOST):$($env:APP_PORT)"
Write-Host "Python: $PythonBin"
Write-Host "Laptop URL: http://127.0.0.1:$($env:APP_PORT)/"
if ($env:APP_HOST -eq "0.0.0.0" -or ($LanIp -and $env:APP_HOST -eq $LanIp)) {
    Write-Host "Phone URL:  http://$($LanIp):$($env:APP_PORT)/"
}
else {
    Write-Host "Phone URL:  unavailable while APP_HOST=$($env:APP_HOST); use APP_HOST=0.0.0.0 for same-Wi-Fi phone testing."
}

& $PythonBin -c "import uvicorn" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Missing Python dependency: uvicorn."
    Write-Host "Install dependencies with: $PythonBin -m pip install -r requirements.txt"
    Write-Host "If this picked the wrong Python, set `$env:PYTHON_BIN = `"/path/to/python3`" before running this script."
    exit 1
}

$AppTarget = "app.main:app"
if (-not (Test-Path "app/main.py") -and (Test-Path "main.py")) {
    $AppTarget = "main:app"
}

$Arguments = @("-m", "uvicorn", $AppTarget, "--host", $env:APP_HOST, "--port", $env:APP_PORT)
if ($env:APP_RELOAD -eq "true") {
    $Arguments += "--reload"
}

& $PythonBin @Arguments
