from pathlib import Path

from invoke import Collection, task

import tp_yass
from tp_yass.tests.helper import get_ini_settings
from .helper import find_ini_file


@task(name='delete', optional=['ini_file'])
def file_delete(c, ini_file=None):
    """刪除上傳的檔案"""

    if ini_file is None:
        ini_file = find_ini_file()

    page_upload_dir = Path(tp_yass.__file__).parent / 'themes' / 'default' / 'static' / 'uploads' / 'pages'
    for each_file in page_upload_dir.glob('*'):
        if each_file.name == '.gitkeep':
            continue
        else:
            each_file.unlink()
