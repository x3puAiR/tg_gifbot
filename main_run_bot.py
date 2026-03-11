''''''

import os
import shutil

from global_config.environment_config import _base_dir, _temp_dir
from telegram_bot.bot_executor import BotExecutor


def _clean_temp_dir():
    if os.path.isdir(_temp_dir):
        shutil.rmtree(_temp_dir)
    os.makedirs(_temp_dir)


if __name__ == '__main__':
    print('Initializing Telegram GIF Bot...')
    _clean_temp_dir()
    print('Loading configuration and dependencies...')
    
    # cert_path = os.path.join(_base_dir, '.openssl/cert.pem')
    # key_path = os.path.join(_base_dir, '.openssl/private.key')
    # webhook_url = 'https://YOUR_DOMAIN:8443/gifbot'
    # BotExecutor(cert_path=cert_path,
    #             key_path=key_path,
    #             webhook_url=webhook_url).execute()
    
    BotExecutor().execute()
