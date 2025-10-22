''''''

import os

# Reads bot token from environment. Fallback to empty to raise clear error later.
_telegrambot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')


