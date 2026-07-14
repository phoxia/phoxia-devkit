$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Get-Command py -ErrorAction SilentlyContinue
if ($Python) { & py -3 (Join-Path $Root "tools\phoxia_devkit.py") install @args; exit $LASTEXITCODE }
$Python = Get-Command python -ErrorAction SilentlyContinue
if ($Python) { & python (Join-Path $Root "tools\phoxia_devkit.py") install @args; exit $LASTEXITCODE }
throw "Python 3 is required."
