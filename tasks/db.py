import re

from invoke import Collection, task

from tp_yass.tests.helper import get_ini_settings, import_test_db_data
from .helper import find_ini_file


@task(name='create', optional=['ini_file'])
def db_create(c, ini_file=None):
    """建立資料庫"""

    if ini_file is None:
        ini_file = find_ini_file()

    # Find database name via ini file
    sqlalchemy_url = get_ini_settings(ini_file)['sqlalchemy.url']
    db_name = re.findall(r'/(\w+)\?', sqlalchemy_url)[0]
    db_user, db_pass = re.findall(r'//(\w+):(\w+)@', sqlalchemy_url)[0]
    c.run(f'sudo mysql -uroot -e "CREATE DATABASE IF NOT EXISTS {db_name} '
           'CHARSET utf8mb4"')
    c.run(f'sudo mysql -uroot -e "CREATE USER IF NOT EXISTS {db_user}@localhost '
          f'IDENTIFIED BY \'{db_pass}\'"')
    c.run(f'sudo mysql -uroot -e "GRANT ALL ON {db_name}.* '
          f'TO {db_user}@localhost"')


@task(name='delete', optional=['ini_file'])
def db_delete(c, ini_file=None):
    """刪除資料庫"""

    if ini_file is None:
        ini_file = find_ini_file()

    sqlalchemy_url = get_ini_settings(ini_file)['sqlalchemy.url']
    db_name = re.findall(r'/(\w+)\?', sqlalchemy_url)[0]
    c.run(f'sudo mysql -uroot -e "DROP DATABASE IF EXISTS {db_name}"')


@task(db_create, name='init', optional=['ini_file'])
def init_db(c, ini_file=None):
    """匯入初始資料至資料庫"""

    if ini_file is None:
        ini_file = find_ini_file()

    c.run(f'alembic -c {ini_file} upgrade head')
    c.run(f'initialize_tp_yass_db {ini_file}')


@task(db_delete, db_create, init_db, name='init-test', optional=['ini_file'])
def init_test_db(c, ini_file=None):
    """匯入開發測試用的初始資料"""

    if ini_file is None:
        ini_file = find_ini_file()

    c.run(f'alembic -c {ini_file} upgrade head')
    import_test_db_data(ini_file)


@task(name='upgrade', optional=['ini_file'])
def db_upgrade(c, ini_file=None):
    """將資料庫 migrate 至最新版"""

    if ini_file is None:
        ini_file = find_ini_file()

    c.run(f'alembic -c {ini_file} upgrade head')


@task(name='downgrade', optional=['ini_file'])
def db_downgrade(c, ini_file=None):
    """將資料庫 downgrade 至前一版"""

    if ini_file is None:
        ini_file = find_ini_file()

    c.run(f'alembic -c {ini_file} downgrade -1')
