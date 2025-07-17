import sys
import json
import argparse

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from .. import models
from ..helpers.backend.theme_config import ThemeController
from ..enum import NavbarType, EmailType


def setup_models(dbsession):
    """
    Add or update models / fixtures in the database.

    """

    # 建立根群組
    root_group = models.account.GroupModel(name='根群組', type=2, depth=1)
    dbsession.add(root_group)

    # 建立管理者 Email
    admin_email = models.account.EmailModel(address='webmaster@example.org', type=EmailType.USER_PRIMARY.value)


    # 建立管理者帳號
    group = models.account.GroupModel(name='最高管理者群組', type=0, ancestor=root_group, depth=2)
    user = models.account.UserModel(first_name='管理者',
                                 last_name='最高',
                                 email=[admin_email],
                                 account='admin',
                                 password='admin4yascms',
                                 groups=[group])
    dbsession.add(group)
    dbsession.add(user)

    # 建立基本系統設定值
    dbsession.add(models.global_config.GlobalConfigModel(name='site_name', value='', type='str', description='設定全名'))
    dbsession.add(models.global_config.GlobalConfigModel(name='site_slogan', value='', type='str', description='設定標語'))
    dbsession.add(models.global_config.GlobalConfigModel(name='theme_name', value='yascms2020', type='str', description='設定啟用的樣板'))
    dbsession.add(models.global_config.GlobalConfigModel(name='site_phone', value='', type='str', description='設定電話，比如 85021571'))
    dbsession.add(models.global_config.GlobalConfigModel(name='site_fax', value='', type='str', description='設定傳真電話，比如 85011146'))
    dbsession.add(models.global_config.GlobalConfigModel(name='site_email', value='', type='str', description='設定聯絡 Email'))
    dbsession.add(models.global_config.GlobalConfigModel(name='site_zip', value='', type='int', description='設定郵遞區號'))
    dbsession.add(models.global_config.GlobalConfigModel(name='site_address', value='', type='str', description='設定地址'))
    dbsession.add(models.global_config.GlobalConfigModel(name='site_map_url', value='', type='str', description='設定地圖網址'))
    dbsession.add(models.global_config.GlobalConfigModel(name='site_map_embedded_url', value='', type='str', description='設定地圖的嵌入網址'))

    # 此唯讀設定用來後台備份或升級用，不該顯示在畫面上讓使用者可以調整
    dbsession.add(models.global_config.GlobalConfigModel(name='sys_maint_mode', value='False', type='bool', description='設定全站是否唯讀'))

    # oauth2 整合的設定，以 json 格式存放
    oauth2_config = {'google': {'canonical_name': 'Google',
                                'access_token_uri': 'https://www.googleapis.com/oauth2/v4/token',
                                'authorization_url': 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline',
                                'settings': {'enabled': False,
                                             'client_id': '',
                                             'client_secret': ''}}}
    dbsession.add(models.global_config.GlobalConfigModel(name='oauth2_integration', value=json.dumps(oauth2_config, ensure_ascii=False), type='str', description='OAuth2 整合設定'))

    dbsession.add(models.global_config.GlobalConfigModel(name='site_builtin_auth', value='True', type='bool', description='設定是否啟用內建的帳號認證'))


    # 匯入預設樣板 yascms2020 的佈景主題設定檔
    theme_importer = ThemeController('yascms2020')
    theme_importer.import_theme()

    # 預先建立單一頁面，以讓後面建立的 navbar 可以進行連結
    dbsession.add(models.PageModel(id=1, title='學校歷史', content=''))
    dbsession.add(models.PageModel(id=2, title='特色課程', content=''))
    dbsession.add(models.PageModel(id=3, title='班群教室', content=''))
    dbsession.add(models.PageModel(id=4, title='校長室', content=''))
    dbsession.add(models.PageModel(id=5, title='教務處', content=''))
    dbsession.add(models.PageModel(id=6, title='學務處', content=''))
    dbsession.add(models.PageModel(id=7, title='輔導室', content=''))
    dbsession.add(models.PageModel(id=8, title='總務處', content=''))
    dbsession.add(models.PageModel(id=9, title='幼兒園', content=''))
    dbsession.add(models.PageModel(id=10, title='資訊中心', content=''))
    dbsession.add(models.PageModel(id=11, title='校內服務', content=''))
    dbsession.add(models.PageModel(id=12, title='課後社團報名', content=''))

    # 建立導覽列的預設順序
    # 最上層，前台不該顯示，但後台在調整 navbar 階層位置時需要顯示
    root = models.navbar.NavbarModel(name='根導覽列', aria_name='root', type=int(NavbarType.TREE_NODE), module_name='root')
    dbsession.add(root)
    # 最新消息
    dbsession.add(models.navbar.NavbarModel(name='最新消息', aria_name='news', order=1, type=int(NavbarType.BUILTIN_NEWS), module_name='news', icon='bi-megaphone', ancestor=root))
    # 學校簡介
    school_intro = models.navbar.NavbarModel(name='學校簡介', aria_name='introduction', order=2, type=int(NavbarType.TREE_NODE), icon='bi-house', ancestor=root)
    dbsession.add(school_intro)
    dbsession.add(models.navbar.NavbarModel(name='學校歷史', order=1, type=int(NavbarType.LEAF_NODE), page_id=1, ancestor=school_intro))
    dbsession.add(models.navbar.NavbarModel(name='特色課程', order=2, type=int(NavbarType.LEAF_NODE), page_id=2, ancestor=school_intro))
    dbsession.add(models.navbar.NavbarModel(name='班群教室', order=3, type=int(NavbarType.LEAF_NODE), page_id=3, ancestor=school_intro))
    dbsession.add(models.navbar.NavbarModel(name='分隔線', order=4, type=int(NavbarType.DROPDOWN_DIVIDER), ancestor=school_intro))
    dbsession.add(models.navbar.NavbarModel(name='分機表', order=5, type=int(NavbarType.BUILTIN_TELEXT), icon='bi-telephone', module_name='telext', ancestor=school_intro))
    # 校園單位
    school_org = models.navbar.NavbarModel(name='組織架構', aria_name='organization', order=3, type=int(NavbarType.TREE_NODE), icon='bi-building', ancestor=root)
    dbsession.add(school_org)
    dbsession.add(models.navbar.NavbarModel(name='校長室', order=1, type=int(NavbarType.LEAF_NODE), page_id=4, ancestor=school_org))
    dbsession.add(models.navbar.NavbarModel(name='教務處', order=2, type=int(NavbarType.LEAF_NODE), page_id=5, ancestor=school_org))
    dbsession.add(models.navbar.NavbarModel(name='學務處', order=3, type=int(NavbarType.LEAF_NODE), page_id=6, ancestor=school_org))
    dbsession.add(models.navbar.NavbarModel(name='輔導室', order=4, type=int(NavbarType.LEAF_NODE), page_id=7, ancestor=school_org))
    dbsession.add(models.navbar.NavbarModel(name='總務處', order=5, type=int(NavbarType.LEAF_NODE), page_id=8, ancestor=school_org))
    dbsession.add(models.navbar.NavbarModel(name='幼兒園', order=6, type=int(NavbarType.LEAF_NODE), page_id=9, ancestor=school_org))
    # 師生園地
    school_garden = models.navbar.NavbarModel(name='師生園地', aria_name='garden', order=4, type=int(NavbarType.TREE_NODE), icon='bi-sun', ancestor=root)
    dbsession.add(school_garden)
    dbsession.add(models.navbar.NavbarModel(name='資訊中心', order=1, type=int(NavbarType.LEAF_NODE), page_id=10, ancestor=school_garden))
    dbsession.add(models.navbar.NavbarModel(name='校內服務', order=2, type=int(NavbarType.LEAF_NODE), page_id=11, ancestor=school_garden))
    dbsession.add(models.navbar.NavbarModel(name='課後社團報名', order=3, type=int(NavbarType.LEAF_NODE), page_id=12, ancestor=school_garden, is_href_blank=True))
    dbsession.add(models.navbar.NavbarModel(name='分隔線', order=4, type=int(NavbarType.DROPDOWN_DIVIDER), ancestor=school_garden))
    # 外站連結
    outside_link = models.navbar.NavbarModel(name='外站連結', aria_name='links', order=5, type=int(NavbarType.TREE_NODE), icon='bi-link-45deg', ancestor=root)
    dbsession.add(outside_link)
    dbsession.add(models.navbar.NavbarModel(name='臺北市政府教育局', order=1, type=int(NavbarType.LEAF_NODE), icon='bi-bookmark', ancestor=outside_link, url='https://www.doe.gov.taipei/'))
    dbsession.add(models.navbar.NavbarModel(name='臺北市政府', order=2, type=int(NavbarType.LEAF_NODE), icon='bi-bookmark', ancestor=outside_link, url='https://www.gov.taipei'))
    dbsession.add(models.navbar.NavbarModel(name='分隔線', order=4, type=int(NavbarType.DROPDOWN_DIVIDER), ancestor=outside_link))
    dbsession.add(models.navbar.NavbarModel(name='好站連結', order=5, type=int(NavbarType.BUILTIN_LINKS), icon='bi-link', module_name='links', ancestor=outside_link))

    # 建立預設的最新消息分類群組
    dbsession.add(models.news.NewsCategoryModel(name='行政公告'))
    dbsession.add(models.news.NewsCategoryModel(name='學校榮譽'))
    dbsession.add(models.news.NewsCategoryModel(name='教師甄試'))

    # 建立預設的好站連結群組
    dbsession.add(models.link.LinkCategoryModel(name='未分類'))

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
初始化資料庫資料失敗，可能有以下原因：

1. 還沒建立資料庫，通常你不應該直接執行 initialize_yascms_db 指令，
   取而代之的應該是執行 inv db.upgrade 才是完整初始化的步驟。

2. 尚未啟動資料庫，請先啟動資料庫後再執行資料庫初始化的指令 inv db.upgrade 。
''')
