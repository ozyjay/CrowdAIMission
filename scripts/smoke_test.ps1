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

$EnvAppPort = $env:APP_PORT
Import-DotEnv ".env"
if ($EnvAppPort) { $env:APP_PORT = $EnvAppPort }
if (-not $env:APP_PORT) { $env:APP_PORT = "3200" }

$BaseUrl = "http://127.0.0.1:$($env:APP_PORT)"
$Paths = @(
    "/",
    "/ping",
    "/screen",
    "/staff",
    "/health",
    "/replay",
    "/api/state",
    "/api/missions",
    "/qr.svg"
)

foreach ($Path in $Paths) {
    $Url = "$BaseUrl$Path"
    Write-Host "Checking $Url"
    try {
        Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2 | Out-Null
    }
    catch {
        Write-Host "Smoke test failed for $Url"
        throw
    }
}

Write-Host "Smoke test passed."
