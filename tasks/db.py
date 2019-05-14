import re

from invoke import Collection, task

from tp_yass.tests.helper import get_ini_settings, import_test_db_data


@task(name='create')
def db_create(c, ini_file):
    """Create database"""
    # Find database name via ini file
    sqlalchemy_url = get_ini_settings(ini_file)['sqlalchemy.url']
    db_name = re.findall(r'/(\w+)\?', sqlalchemy_url)[0]
    db_user, db_pass = re.findall(r'//(\w+):(\w+)@', sqlalchemy_url)[0]
    c.run('sudo mysql -uroot -e "CREATE DATABASE IF NOT EXISTS {} CHARSET utf8mb4"'.format(db_name))
    c.run('sudo mysql -uroot -e "GRANT ALL ON {0}.* to {1}@localhost '
          'IDENTIFIED BY \'{2}\'"'.format(db_name, db_user, db_pass))


@task(name='delete')
def db_delete(c, ini_file):
    """Delete database"""
    sqlalchemy_url = get_ini_settings(ini_file)['sqlalchemy.url']
    db_name = re.findall(r'/(\w+)\?', sqlalchemy_url)[0]
    c.run('sudo mysql -uroot -e "DROP DATABASE IF EXISTS {}"'.format(db_name))


@task(db_create, name='init')
def init_db(c, ini_file):
    """Create database and import basic data"""
    c.run('alembic -c {} upgrade head'.format(ini_file))
    c.run('initialize_tp_yass_db {}'.format(ini_file))


@task(db_delete, db_create, name='init-test')
def init_test_db(c, ini_file):
    """Create database and import test data"""
    c.run('alembic -c {} upgrade head'.format(ini_file))
    import_test_db_data(ini_file)


@task(name='upgrade', optional=['ini_file'])
def db_upgrade(c, ini_file=None):
    """將 db migrate 至最新版"""

    if ini_file is None:
        if os.path.exists('production.ini'):
            ini_file = 'production.ini'
        elif os.path.exists('development.ini'):
            ini_file = 'development.ini'
        else:
            raise ParseError('--ini-file 必須指定合法的 ini 設定檔')

    c.run('alembic -c {} upgrade head'.format(ini_file))


@task(name='downgrade', optional=['ini_file'])
def db_downgrade(c, ini_file=None):
    """將 db downgrade 至前一版"""

    if ini_file is None:
        if os.path.exists('production.ini'):
            ini_file = 'production.ini'
        elif os.path.exists('development.ini'):
            ini_file = 'development.ini'
        else:
            raise ParseError('--ini-file 必須指定合法的 ini 設定檔')

    c.run('alembic -c {} downgrade -1'.format(ini_file))

