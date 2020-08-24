from glob import glob
from pathlib import Path
import subprocess

from invoke import Collection, task

import tp_yass
from tp_yass.tests.helper import get_ini_settings
from .helper import find_ini_file


@task(name='delete', optional=['ini_file'])
def file_delete(c, ini_file=None):
    """刪除上傳的檔案"""

    if ini_file is None:
        ini_file = find_ini_file()

    page_upload_dir = Path(tp_yass.__file__).parent / 'uploads'
    for each_subdir in ['links', 'news', 'pages']:
        dest_dir = page_upload_dir / each_subdir / '*'
        subprocess.run(f'rm -rf {dest_dir}', shell=True)
