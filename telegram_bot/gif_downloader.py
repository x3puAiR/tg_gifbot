''''''

import os
from telegram import Bot

from global_config.protected_config import _telegrambot_token
from global_config.environment_config import _temp_dir
from telegram_bot.func_helper import random_string, zip_dir, ensure_directory, mp42gif


# Video conversion settings
GIF_FRAME_RATE_FPS = 10


class GifDownloader():
    """Download and convert GIF files from Telegram documents to PNG sequences."""

    def __init__(self):
        """Initialize the GIF downloader with Telegram bot API access."""
        self.bot = Bot(_telegrambot_token)

    def download_gif(self, file_id, save_dir=None, random_name=False):
        """Download a GIF file from Telegram and convert it to animated GIF format."""
        try:
            gif = file_id if not isinstance(file_id, str) else self.bot.get_file(file_id)

            # use default `temp` path
            save_dir = save_dir or _temp_dir
            file_name = gif.file_path.split('/')[-1]
            if random_name:
                file_name = random_string() + '.mp4'
            file_path = os.path.join(save_dir, file_name)
            out_path = file_path.replace('mp4', 'gif')

            # download and convert
            gif.download(custom_path=file_path)
            mp42gif(file_path, out_path, fps=GIF_FRAME_RATE_FPS)

            return (file_path, out_path)
        except OSError as e:
            raise Exception(f'File I/O error in download_gif: {str(e)}')
        except Exception as e:
            raise Exception(f'Error downloading or converting GIF: {str(e)}')

    def download_gif_pack(self, file_id, pack_name, out_path=None):
        """Download a GIF file and create a zip package for distribution."""
        try:
            # make dir `pack_name`
            file_dir = os.path.join(_temp_dir, pack_name)
            ensure_directory(file_dir)

            # download and convert
            self.download_gif(file_id, save_dir=file_dir, random_name=True)

            # zip
            out_path = out_path or file_dir + '.zip'
            zip_dir(file_dir, out_path)

            return out_path
        except OSError as e:
            raise Exception(f'File system error in download_gif_pack: {str(e)}')
        except Exception as e:
            raise Exception(f'Error creating GIF pack: {str(e)}')


_gif = GifDownloader()
download_gif = _gif.download_gif
download_gif_pack = _gif.download_gif_pack


if __name__ == '__main__':
    pass
