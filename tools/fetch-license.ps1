$ErrorActionPreference = "Stop"
Invoke-WebRequest -Uri "https://www.gnu.org/licenses/agpl-3.0.txt" -OutFile "LICENSE"
Write-Host "Downloaded official GNU AGPL v3 text to LICENSE"
