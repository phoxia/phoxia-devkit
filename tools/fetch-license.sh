#!/usr/bin/env bash
set -euo pipefail
curl --fail --location --proto '=https' --tlsv1.2   https://www.gnu.org/licenses/agpl-3.0.txt   --output LICENSE
echo "Downloaded official GNU AGPL v3 text to LICENSE"
