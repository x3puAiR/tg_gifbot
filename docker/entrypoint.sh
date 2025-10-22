#!/usr/bin/env bash
set -euo pipefail

# Ensure virtualenv exists to align with install script expectations
if [ ! -d "/app/.env" ]; then
  python3 -m venv /app/.env || true
fi
source /app/.env/bin/activate || true
pip3 install -r requirements.txt


# Generate config files based on env vars
mkdir -p /app/global_config

# protected_config.py uses env sourcing by default, but keep compatibility
cat > /app/global_config/protected_config.py <<'PY'
import os
_telegrambot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
PY

# environment_config.py for base and temp dirs
BASE_DIR=${BASE_DIR:-/app}
TEMP_DIR=${TEMP_DIR:-/data}
cat > /app/global_config/environment_config.py <<PY
_base_dir = '${BASE_DIR}'
_temp_dir = '${TEMP_DIR}'
PY

mkdir -p "${TEMP_DIR}" 

exec "$@"


