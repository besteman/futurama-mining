$processToCheck = "nanominer"

$process = Get-Process $processToCheck -ErrorAction SilentlyContinue

if ($null -eq $process) {
    Write-Host $process
    & "C:\Users\hyrule\Desktop\nanominer-windows-3.1.5-cuda11\nanominer.exe"
}
