import re

from invoke import task

from tp_yass.tests.helper import get_ini_settings, import_test_db_data


@task
def deploy(c, ini_file):
    """Deploy project"""

    c.run('git pull origin master')
    c.run('pipenv sync')
    c.run('alembic -c {} upgrade head'.format(ini_file))
    c.run('systemctl restart uwsgi')


@task
def create_db(c, ini_file):
    """Create database"""

    # Find database name via ini file
    sqlalchemy_url = get_ini_settings(ini_file)['sqlalchemy.url']
    db_name = re.findall(r'/(\w+)\?', sqlalchemy_url)[0]
    db_user, db_pass = re.findall(r'//(\w+):(\w+)@', sqlalchemy_url)[0]
    c.run('sudo mysql -uroot -e "CREATE DATABASE IF NOT EXISTS {} CHARSET utf8mb4"'.format(db_name))
    c.run('sudo mysql -uroot -e "GRANT ALL ON {0}.* to {1}@localhost '
          'IDENTIFIED BY \'{2}\'"'.format(db_name, db_user, db_pass))


@task
def delete_db(c, ini_file):
    """Delete database"""
    sqlalchemy_url = get_ini_settings(ini_file)['sqlalchemy.url']
    db_name = re.findall(r'/(\w+)\?', sqlalchemy_url)[0]
    c.run('sudo mysql -uroot -e "DROP DATABASE IF EXISTS {}"'.format(db_name))


@task(create_db)
def init_db(c, ini_file):
    """Create database and import basic data"""

    c.run('alembic -c {} upgrade head'.format(ini_file))
    c.run('initialize_tp_yass_db {}'.format(ini_file))


@task(delete_db, create_db)
def init_test_db(c, ini_file):
    """Create database and import test data"""

    c.run('alembic -c {} upgrade head'.format(ini_file))
    import_test_db_data(ini_file)


@task
def test(c):
    c.run('pytest')


@task
def test_coverage(c):
    c.run('pytest --cov=tp_yass')
