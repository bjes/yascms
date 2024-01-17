import os, re

from invoke import Collection, task
from invoke.exceptions import ParseError

from yascms.tests.helper import get_ini_settings, import_test_db_data

from . import db, test, file, doc
from .helper import find_ini_file


@task(optional=['ini_file'])
def deploy(c, ini_file=None):
    """佈署此專案"""

    if ini_file is None:
        ini_file = find_ini_file()

    c.run('git pull origin master')
    c.run('systemctl stop uwsgi')
    c.run(f'alembic -c {ini_file} upgrade head')
    c.run('poetry install')
    c.run('systemctl start uwsgi')


namespace = Collection(deploy, db, test, file, doc)

