''''''

import os
from PIL import Image
from telegram import Bot

from global_config.protected_config import _telegrambot_token
from global_config.environment_config import _temp_dir
from telegram_bot.func_helper import random_string, zip_dir, ensure_directory, mp42gif


# Sticker conversion settings
STICKER_FRAME_RATE_FPS = 30


class StickerSetDownloader():
    """Download and convert Telegram sticker sets to PNG format."""

    def __init__(self):
        """Initialize the sticker set downloader with Telegram bot API access."""
        self.num_threads = 4
        self.bot = Bot(_telegrambot_token)

    @staticmethod
    def webp2png(in_file_path, out_file_path):
        """Convert WebP image to PNG format using PIL."""
        im = Image.open(in_file_path)
        im.save(out_file_path, 'PNG')
        return out_file_path

    @staticmethod
    def webm2gif(in_file_path, out_file_path):
        """Convert WebM video to animated GIF using ffmpeg with palette for accurate speed."""
        import logging
        logger = logging.getLogger('gifbot')

        # Two-pass palette approach: preserves colour quality and correct playback speed.
        # fps=30 matches Telegram sticker frame rate closely while staying within GIF's
        # ~50fps renderer ceiling (most players floor frame delay to 20ms).
        palette_path = out_file_path.replace('.gif', '_palette.png')
        vf_palette = 'fps=30,scale=256:-1:flags=lanczos,palettegen'
        vf_render  = 'fps=30,scale=256:-1:flags=lanczos[x];[x][1:v]paletteuse'

        cmd_palette = 'ffmpeg -y -i %(in)s -vf "%(vf)s" %(palette)s' % {
            'in': in_file_path, 'vf': vf_palette, 'palette': palette_path}
        cmd_render  = 'ffmpeg -y -i %(in)s -i %(palette)s -filter_complex "%(vf)s" %(out)s' % {
            'in': in_file_path, 'palette': palette_path, 'vf': vf_render, 'out': out_file_path}

        logger.debug('WebM to GIF palette command: %s', cmd_palette)
        status = os.system(cmd_palette + ' > /dev/null 2>&1')

        if status == 0:
            logger.debug('WebM to GIF render command: %s', cmd_render)
            status = os.system(cmd_render + ' > /dev/null 2>&1')
            os.path.isfile(palette_path) and os.remove(palette_path)

        if status != 0:
            # Fallback: single-pass, no palette (slightly worse quality but still correct speed)
            os.path.isfile(palette_path) and os.remove(palette_path)
            cmd_fallback = 'ffmpeg -y -i %(in)s -vf "fps=30,scale=256:-1" %(out)s' % {
                'in': in_file_path, 'out': out_file_path}
            logger.debug('WebM to GIF fallback command: %s', cmd_fallback)
            status = os.system(cmd_fallback + ' > /dev/null 2>&1')
            if status != 0:
                logger.error('WebM to GIF conversion failed with status: %s', status)
                raise Exception('ffmpeg error: execute .webm => .gif')

        logger.debug('WebM to GIF conversion completed successfully')
        return out_file_path

    @staticmethod
    def webm2png(in_file_path, out_file_path):
        """Extract first frame from WebM video and convert to PNG using ffmpeg."""
        # Use ffmpeg to extract first frame from WebM video and convert to PNG
        command = 'ffmpeg -y -i %(webm)s -vframes 1 -f image2 %(png)s > /dev/null 2>&1'
        command = command % {'webm': in_file_path, 'png': out_file_path}
        status = os.system(command)
        if status != 0:
            raise Exception('ffmpeg error: execute .webm => .png')
        else:
            return out_file_path

    @staticmethod
    def tgs2mp4(in_file_path, out_file_path):
        """Convert TGS animated sticker to MP4 video using tgsconvert and puppeteer-lottie."""
        json_path = out_file_path.replace('mp4', 'json')
        command = 'tgsconvert.py %(tgs)s %(json)s > /dev/null 2>&1'
        command = command % {'tgs': in_file_path, 'json': json_path}
        status = os.system(command)
        if status != 0:
            os.path.isfile(json_path) and os.remove(json_path)
            raise Exception('tgsconvert.py error: execute .tgs => .json')

        command = 'puppeteer-lottie -q -i %(json)s -o %(mp4)s > /dev/null 2>&1'
        command = command % {'json': json_path, 'mp4': out_file_path}
        status = os.system(command)
        os.path.isfile(json_path) and os.remove(json_path)
        if status != 0:
            raise Exception('puppeteer-lottie error: execute .json => .mp4')
        else:
            return out_file_path


    def download_sticker(self, file_id, save_dir=None, random_name=False):
        """Download a sticker from Telegram and convert to PNG format."""
        try:
            sticker = file_id if not isinstance(file_id, str) else self.bot.get_file(file_id)

            # use default `temp` path
            save_dir = save_dir or _temp_dir
            file_name = sticker.file_path.split('/')[-1]

            # Determine file extension from the actual file path
            file_extension = os.path.splitext(file_name)[1].lower()

            if random_name:
                # Use the actual file extension instead of assuming .webp
                file_name = random_string() + file_extension

            file_path = os.path.join(save_dir, file_name)

            # Determine output path based on file type
            if file_extension == '.webm':
                out_path = file_path.replace('.webm', '.gif')  # WebM converts to animated GIF
            elif file_extension == '.webp':
                out_path = file_path.replace('.webp', '.png')
            else:
                # For other formats, try to convert to PNG
                out_path = file_path.replace(file_extension, '.png')

            # download the file
            sticker.download(custom_path=file_path)

            # convert based on file type
            if file_extension == '.webm':
                self.webm2gif(file_path, out_path)
            elif file_extension == '.webp':
                self.webp2png(file_path, out_path)
            else:
                # Try PIL first, fallback to ffmpeg if PIL fails
                try:
                    self.webp2png(file_path, out_path)
                except Exception as pil_err:
                    # If PIL fails, try ffmpeg as fallback
                    try:
                        self.webm2png(file_path, out_path)
                    except Exception:
                        raise Exception(f'Failed to convert sticker format {file_extension}: {str(pil_err)}')

            return (file_path, out_path)
        except OSError as e:
            raise Exception(f'File I/O error in download_sticker: {str(e)}')
        except Exception as e:
            raise Exception(f'Error downloading or converting sticker: {str(e)}')

    def download_sticker_set(self, sticker_set_name, out_path=None):
        """Download an entire sticker set from Telegram and create a zip package."""
        try:
            sticker_set = self.bot.get_sticker_set(sticker_set_name)
            stickers = sticker_set.stickers

            # make dir `sticker_set_name`
            file_dir = os.path.join(_temp_dir, sticker_set_name)
            ensure_directory(file_dir)

            # download and convert
            for sticker in stickers:
                try:
                    file_id = sticker.file_id
                    self.download_sticker(file_id, save_dir=file_dir, random_name=True)
                except OSError as e:
                    raise Exception(f'File error processing sticker {file_id}: {str(e)}')

            # zip
            out_path = out_path or file_dir + '.zip'
            zip_dir(file_dir, out_path)
            return out_path
        except OSError as e:
            raise Exception(f'File system error in download_sticker_set: {str(e)}')
        except Exception as e:
            raise Exception(f'Error downloading sticker set: {str(e)}')

    def download_sticker_animated(self, file_id, save_dir=None, random_name=False):
        """Download an animated sticker and convert to GIF format."""
        try:
            sticker = file_id if not isinstance(file_id, str) else self.bot.get_file(file_id)

            # use default `temp` path
            save_dir = save_dir or _temp_dir
            file_name = sticker.file_path.split('/')[-1]
            if random_name:
                file_name = random_string() + '.tgs'
            file_path = os.path.join(save_dir, file_name)
            out_path_mp4 = file_path.replace('tgs', 'mp4')
            out_path_gif = file_path.replace('tgs', 'gif')

            # download and convert
            sticker.download(custom_path=file_path)
            self.tgs2mp4(file_path, out_path_mp4)
            mp42gif(out_path_mp4, out_path_gif, fps=STICKER_FRAME_RATE_FPS)

            return (file_path, out_path_mp4, out_path_gif)
        except OSError as e:
            raise Exception(f'File I/O error in download_sticker_animated: {str(e)}')
        except Exception as e:
            raise Exception(f'Error downloading or converting animated sticker: {str(e)}')

    def download_sticker_animated_pack(self, file_id, pack_name, out_path=None):
        """Download an animated sticker and create a zip package."""
        try:
            # make dir `pack_name`
            file_dir = os.path.join(_temp_dir, pack_name)
            ensure_directory(file_dir)

            # download and convert
            self.download_sticker_animated(file_id, save_dir=file_dir, random_name=True)

            # zip
            out_path = out_path or file_dir + '.zip'
            zip_dir(file_dir, out_path)

            return out_path
        except OSError as e:
            raise Exception(f'File system error in download_sticker_animated_pack: {str(e)}')
        except Exception as e:
            raise Exception(f'Error creating animated sticker pack: {str(e)}')


_sticker = StickerSetDownloader()
download_sticker = _sticker.download_sticker
download_sticker_set = _sticker.download_sticker_set
download_sticker_animated_pack = _sticker.download_sticker_animated_pack


if __name__ == '__main__':
    pass
