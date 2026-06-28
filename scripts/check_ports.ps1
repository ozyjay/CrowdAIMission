$ErrorActionPreference = "Stop"

$Ports = @(3200, 8200, 8600, 8700, 8800)

foreach ($Port in $Ports) {
    $Client = [System.Net.Sockets.TcpClient]::new()
    try {
        $Connection = $Client.BeginConnect("127.0.0.1", $Port, $null, $null)
        $InUse = $Connection.AsyncWaitHandle.WaitOne(300)
        if ($InUse) {
            $Client.EndConnect($Connection)
            Write-Host "Port $Port is already in use."
            exit 1
        }
    }
    catch {
        # Connection refused means the port is available.
    }
    finally {
        $Client.Close()
    }

    Write-Host "Port $Port OK"
}
