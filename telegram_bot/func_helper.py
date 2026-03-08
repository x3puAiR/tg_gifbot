"""Helper functions for file operations and utilities."""

import os
import zipfile
from random import shuffle

# Video conversion settings (default for general GIF conversion)
MP4_TO_GIF_DEFAULT_FPS = 10


def random_string(length=8):
    """Generate a random alphanumeric string of specified length."""
    s = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    s_length = 62
    while length > s_length:
        s += s
        s_length += 62
    s_list = list(s)
    shuffle(s_list)
    return ''.join(s_list[:length])

def zip_dir(in_file_dir, out_file_path):
    """Create a compressed zip archive from a directory."""
    f = zipfile.ZipFile(out_file_path, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(in_file_dir):
        fpath = dirpath.replace(in_file_dir, '')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            f.write(os.path.join(dirpath, filename), fpath+filename)
    f.close()

def extract_filename_and_ext(file_path):
    """Extract filename and extension from a file path.

    Returns:
        tuple: (filename_without_extension, extension)
    """
    file_name = file_path.split('/')[-1]
    name_parts = file_name.split('.')
    extension = '.' + name_parts[-1] if len(name_parts) > 1 else ''
    filename = '.'.join(name_parts[:-1]) if extension else file_name
    return (filename, extension)

def ensure_directory(dir_path):
    """Create directory if it doesn't exist.

    Args:
        dir_path: Path to the directory

    Returns:
        bool: True if directory exists or was created successfully
    """
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    return True

def mp42gif(in_file_path, out_file_path, fps=MP4_TO_GIF_DEFAULT_FPS):
    """Convert MP4 video to animated GIF using ffmpeg with palette generation.

    Args:
        in_file_path: Path to input MP4 file
        out_file_path: Path to output GIF file
        fps: Frames per second for the GIF (default: 10)

    Returns:
        str: Path to the output GIF file

    Raises:
        Exception: If ffmpeg conversion fails
    """
    palette_path = out_file_path.replace('.gif', '_palette.png')
    command = f'ffmpeg -y -i {in_file_path} -vf fps={fps},scale=-1:-1:flags=lanczos,palettegen {palette_path}'
    status = os.system(command + ' > /dev/null 2>&1')
    if status != 0:
        os.path.isfile(palette_path) and os.remove(palette_path)
        raise Exception('ffmpeg error: execute gif => _palette.png')

    command = f'ffmpeg -y -i {in_file_path} -i {palette_path} -filter_complex "fps={fps},scale=-1:-1:flags=lanczos[x];[x][1:v]paletteuse" {out_file_path}'
    status = os.system(command + ' > /dev/null 2>&1')
    os.path.isfile(palette_path) and os.remove(palette_path)
    if status != 0:
        raise Exception('ffmpeg error: execute .gif => .mp4')
    else:
        return out_file_path
