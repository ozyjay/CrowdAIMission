$ErrorActionPreference = "Stop"

$EnvAppHost = $env:APP_HOST
$EnvAppPort = $env:APP_PORT
$EnvAppReload = $env:APP_RELOAD

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
        $Name = $Parts[0].Trim()
        $Value = $Parts[1].Trim().Trim('"').Trim("'")
        if ($Name) {
            Set-Item -Path "Env:$Name" -Value $Value
        }
    }
}

function Get-LanIp {
    if ($IsMacOS -or $IsLinux) {
        $Ip = (& ipconfig getifaddr en0 2>$null)
        if ($Ip) {
            return $Ip.Trim()
        }

        $Ifconfig = (& ifconfig 2>$null)
        foreach ($Line in $Ifconfig) {
            if ($Line -match "inet\s+(\d+\.\d+\.\d+\.\d+)") {
                $Candidate = $Matches[1]
                if ($Candidate -ne "127.0.0.1") {
                    return $Candidate
                }
            }
        }
    }

    $Address = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
        Where-Object { $_.IPAddress -ne "127.0.0.1" -and $_.PrefixOrigin -ne "WellKnown" } |
        Select-Object -First 1 -ExpandProperty IPAddress
    return $Address
}

Import-DotEnv ".env"

if ($EnvAppHost) {
    $env:APP_HOST = $EnvAppHost
}
if ($EnvAppPort) {
    $env:APP_PORT = $EnvAppPort
}
if ($EnvAppReload) {
    $env:APP_RELOAD = $EnvAppReload
}

if (-not $env:APP_PORT) {
    $env:APP_PORT = "3200"
}
if (-not $env:APP_HOST) {
    $env:APP_HOST = "127.0.0.1"
}
if (-not $env:APP_RELOAD) {
    $env:APP_RELOAD = "false"
}

$LanIp = Get-LanIp

Write-Host "Starting Crowd AI Mission Control dev server on $($env:APP_HOST):$($env:APP_PORT)."
Write-Host "Laptop URL: http://127.0.0.1:$($env:APP_PORT)/"
if ($env:APP_HOST -eq "0.0.0.0" -or ($LanIp -and $env:APP_HOST -eq $LanIp)) {
    if ($LanIp) {
        Write-Host "Phone URL:  http://$($LanIp):$($env:APP_PORT)/"
    }
    else {
        Write-Host "Phone URL:  http://<this-machine-LAN-IP>:$($env:APP_PORT)/"
    }
}
else {
    Write-Host "Phone URL:  unavailable while APP_HOST=$($env:APP_HOST); use APP_HOST=0.0.0.0 for same-Wi-Fi phone testing."
}

$Arguments = @("-m", "uvicorn", "app.main:app", "--host", $env:APP_HOST, "--port", $env:APP_PORT)
if ($env:APP_RELOAD -eq "true") {
    $Arguments += "--reload"
}

& python3 @Arguments
