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
                                 email='webmaster@example.org',
                                 account='admin',
                                 password='admin',
                                 groups=[group])
    dbsession.add(group)
    dbsession.add(user)

    # 建立基本系統設定值
    dbsession.add(models.sys_config.SysConfigModel(name='site_name', value='', description='設定全名'))
    dbsession.add(models.sys_config.SysConfigModel(name='site_slogan', value='', description='設定標語'))
    dbsession.add(models.sys_config.SysConfigModel(name='site_theme', value='tp_yass', description='設定樣板'))
    dbsession.add(models.sys_config.SysConfigModel(name='site_phone', value='', description='設定電話'))
    dbsession.add(models.sys_config.SysConfigModel(name='site_fox', value='', description='設定傳真電話'))
    dbsession.add(models.sys_config.SysConfigModel(name='site_email', value='', description='設定聯絡 Email'))
    dbsession.add(models.sys_config.SysConfigModel(name='site_zip', value='', description='設定郵遞區號'))
    dbsession.add(models.sys_config.SysConfigModel(name='site_address', value='', description='設定地址'))
    dbsession.add(models.sys_config.SysConfigModel(name='site_google_map_url', value='', description='設定 Google Map 網址'))
    dbsession.add(models.sys_config.SysConfigModel(name='site_google_map_embedded_url', value='', description='設定 Google 地圖嵌入網址'))
    dbsession.add(models.sys_config.SysConfigModel(name='site_google_calendar_embedded_url', value='', description='設定 Google 行事曆嵌入網址'))
    # 此唯讀設定用來後台備份或升級用，不該顯示在畫面上讓使用者可以調整
    dbsession.add(models.sys_config.SysConfigModel(name='maintenance_mode', value='false', description='設定全站是否唯讀'))
    dbsession.add(models.sys_config.SysConfigModel(name='homepage_news_quantity', value='20', description='設定首頁顯示幾筆最新消息'))

    # 建立導覽列的預設順序
    # 最新消息
    dbsession.add(models.navbar.NavbarModel(name='最新消息', order=1, type=4, module_name='news', icon='fa-bullhorn'))
    # 學校簡介
    school_intro = models.navbar.NavbarModel(name='學校簡介', order=2, type=1, icon='fa-school')
    dbsession.add(school_intro)
    dbsession.add(models.navbar.NavbarModel(name='學校歷史', order=1, type=2, ancestor=school_intro))
    dbsession.add(models.navbar.NavbarModel(name='特色課程', order=2, type=2, ancestor=school_intro))
    dbsession.add(models.navbar.NavbarModel(name='班群教室', order=3, type=2, ancestor=school_intro))
    dbsession.add(models.navbar.NavbarModel(name='分隔線', order=4, type=3, ancestor=school_intro))
    dbsession.add(models.navbar.NavbarModel(name='行事曆', order=5, type=4, module_name='calendar', ancestor=school_intro))
    dbsession.add(models.navbar.NavbarModel(name='分機表', order=6, type=4, module_name='telext', ancestor=school_intro))
    # 校園單位
    school_org = models.navbar.NavbarModel(name='校園簡介', order=3, type=1, icon='fa-building')
    dbsession.add(school_org)
    dbsession.add(models.navbar.NavbarModel(name='校長室', order=1, type=2, ancestor=school_org))
    dbsession.add(models.navbar.NavbarModel(name='教務處', order=2, type=2, ancestor=school_org))
    dbsession.add(models.navbar.NavbarModel(name='學務處', order=3, type=2, ancestor=school_org))
    dbsession.add(models.navbar.NavbarModel(name='輔導室', order=4, type=2, ancestor=school_org))
    dbsession.add(models.navbar.NavbarModel(name='總務處', order=5, type=2, ancestor=school_org))
    dbsession.add(models.navbar.NavbarModel(name='幼兒園', order=6, type=2, ancestor=school_org))
    # 師生園地
    school_garden = models.navbar.NavbarModel(name='師生園地', order=4, type=1, icon='fa-sun')
    dbsession.add(school_garden)
    dbsession.add(models.navbar.NavbarModel(name='資訊中心', order=1, type=2, ancestor=school_garden))
    dbsession.add(models.navbar.NavbarModel(name='校內服務', order=2, type=2, ancestor=school_garden))
    dbsession.add(models.navbar.NavbarModel(name='課後社團報名', order=3, type=2, ancestor=school_garden, external=True))
    dbsession.add(models.navbar.NavbarModel(name='分隔線', order=4, type=3, ancestor=school_garden))
    dbsession.add(models.navbar.NavbarModel(name='班級網頁', order=5, type=2, ancestor=school_garden, icon='fa-chalkboard-teacher'))
    # 外站連結
    outside_link = models.navbar.NavbarModel(name='外站連結', order=5, type=1, icon='fa-globe-asia')
    dbsession.add(outside_link)
    dbsession.add(models.navbar.NavbarModel(name='臺北市政府教育局', order=1, type=2, icon='fa-university', ancestor=outside_link))
    dbsession.add(models.navbar.NavbarModel(name='臺北市政府', order=2, type=2, icon='fa-globe-asia', ancestor=outside_link))
    dbsession.add(models.navbar.NavbarModel(name='分隔線', order=4, type=3, ancestor=outside_link))
    dbsession.add(models.navbar.NavbarModel(name='好站連結', order=5, type=4, module_name='goodlinks', ancestor=outside_link))
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
