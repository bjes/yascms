import argparse
import sys

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from .. import models


def setup_models(dbsession):
    """
    Add or update models / fixtures in the database.

    """

    # 建立管理者帳號
    group = models.user.GroupModel(name='管理者', type=0)
    user = models.user.UserModel(first_name='管理者',
                                 last_name='管理者',
                                 email='webmaster@xxx.tp.edu.tw',
                                 account='admin',
                                 password='admin',
                                 group=group)
    dbsession.add(group)
    dbsession.add(user)

    # 建立基本系統設定值
    dbsession.add(models.syssettings.SysSettingsModel(name='school_name', value='臺北市中山區無名國小', description='設定學校全名'))
    dbsession.add(models.syssettings.SysSettingsModel(name='maintenance_mode', value='true', description='設定全站是否唯讀'))

    dbsession.commit()


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)
    engine = engine_from_config(env['registry'].settings)
    Session = sessionmaker(bind=engine)
    dbsession = Session()

    try:
        setup_models(dbsession)
    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            ''')
