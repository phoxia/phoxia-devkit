$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
if (Get-Command py -ErrorAction SilentlyContinue) { & py -3 (Join-Path $Root "tools\phoxia_devkit.py") uninstall @args; exit $LASTEXITCODE }
& python (Join-Path $Root "tools\phoxia_devkit.py") uninstall @args
exit $LASTEXITCODE
