def get_ini_settings(ini_file_path):
    """Return ini settings"""
    import plaster

    return plaster.get_settings(ini_file_path, 'app:main')


def import_test_db_data(ini_file_path):
    """Import test data to test database"""
    import json
    import datetime

    from sqlalchemy import engine_from_config
    from sqlalchemy.orm import sessionmaker

    from yascms.models.account import GroupModel, UserModel, EmailModel
    from yascms.models.news import NewsModel, NewsCategoryModel
    from yascms.models.global_config import GlobalConfigModel
    from yascms.models.page import PageModel
    from yascms.models.navbar import NavbarModel
    from yascms.models.theme_config import ThemeConfigModel
    from yascms.enum import NavbarType, HomepageItemType, EmailType, PinnedType

    ini_settings = get_ini_settings(ini_file_path)
    engine = engine_from_config(ini_settings)
    Session = sessionmaker(bind=engine)

    session = Session()

    # 初始化系統設定
    session.query(GlobalConfigModel).filter_by(name='site_name').update({'value': '臺北市中山區濱江國小'})
    session.query(GlobalConfigModel).filter_by(name='site_slogan').update({'value': '快樂學習 - 教學相長'})
    session.query(GlobalConfigModel).filter_by(name='theme_name').update({'value': 'yascms2020'})
    session.query(GlobalConfigModel).filter_by(name='site_phone').update({'value': '85021571'})
    session.query(GlobalConfigModel).filter_by(name='site_fax').update({'value': '85011146'})
    session.query(GlobalConfigModel).filter_by(name='site_email').update({'value': 'public@bjes.tp.edu.tw'})
    session.query(GlobalConfigModel).filter_by(name='site_zip').update({'value': '10462'})
    session.query(GlobalConfigModel).filter_by(name='site_address').update({'value': '臺北市中山區樂群二路266巷99號'})
    session.query(GlobalConfigModel).filter_by(name='site_map_url').update({'value': 'https://goo.gl/maps/X6Y4E37U66aMqQHY6'})
    session.query(GlobalConfigModel).filter_by(name='site_map_embedded_url').update({'value': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3613.7043991522146!2d121.55944821523249!3d25.07800624267944!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3442ac72e5e39d17%3A0x3934b7c47c1bbf29!2zMTA0OTHlj7DljJfluILkuK3lsbHljYDmqILnvqTkuozot68yNjblt7c5OeiZnw!5e0!3m2!1szh-TW!2stw!4v1551164410802'})
    session.commit()

    # 建群組。初始化資料庫時會先建立 root group (id 為 1) 與 admin (id 為 2) 這邊從 3 開始
    group1 = GroupModel(id=3, name='測試國小', type=2, ancestor_id=1, depth=2)
    group2 = GroupModel(id=4, name='教務處', type=1, ancestor_id=3, depth=3)
    group3 = GroupModel(id=5, name='自然領域科任', type=2, ancestor_id=3, depth=3)
    group4 = GroupModel(id=6, name='藝文領域科任', type=2, ancestor_id=3, depth=3)
    group5 = GroupModel(id=7, name='資訊組', type=1, ancestor_id=4, depth=4)
    group6 = GroupModel(id=8, name='系管師', type=1, ancestor_id=4, depth=4)
    # 建帳號。初始化資料庫時會先建立 admin (所以其 id 為 1) 這邊從 2 開始
    user1_email = EmailModel(address='user1@example.org', type=EmailType.USER_PRIMARY.value)
    user1 = UserModel(id=2, first_name='小明', last_name='陳', email=[user1_email],
                      account='user1', password='user1', status=1)
    # user1 群組為資訊組、藝文領域科任
    user1.groups = [group5, group4]
    user2_email = EmailModel(address='user2@example.org', type=EmailType.USER_PRIMARY.value)
    user2 = UserModel(id=3, first_name='大寶', last_name='王', email=[user2_email],
                      account='user2', password='user2', status=1)
    # user2 群組為系管師、自然領域科認
    user2.groups = [group6, group3]
    session.add(group1)
    session.add(group2)
    session.add(group3)
    session.add(group4)
    session.add(group5)
    session.add(group6)
    session.add(user1)
    session.add(user2)

    # 最新消息分類群組
    category1 = session.query(NewsCategoryModel).filter_by(name='行政公告').one_or_none()
    category2 = session.query(NewsCategoryModel).filter_by(name='學校榮譽').one_or_none()

    ######## 建最新消息 ########
    now = datetime.datetime.now()
    # 普通最新消息，永遠顯示
    news1 = NewsModel(id=1, title='採購 10 台伺服器', content='設備已放機房', group_id=6, category=category1)
    # 普通最新消息，超過時間已無法顯示
    news2 = NewsModel(id=2, title='無法顯示的最新消息', content='前台看不到後台看得到', group_id=6, category=category1,
                      visible_start_datetime=now-datetime.timedelta(days=2),
                      display_datetime=now-datetime.timedelta(days=2),
                      visible_end_datetime=now-datetime.timedelta(days=1))
    # 置頂最新消息，今天最後一天置頂，永遠顯示
    news3 = NewsModel(id=3, title='暑假第一天將重灌電腦', content='請老師及早備份資料', group_id=7,
                      is_pinned=PinnedType.IS_PINNED.value, pinned_start_datetime=now-datetime.timedelta(days=1),
                      pinned_end_datetime=now, category=category2)
    # 置頂最新消息，已超過置頂時間，但仍可顯示
    news4 = NewsModel(id=4, title='超過置頂時間的置頂最新消息', content='仍然可顯示', group_id=7,
                      is_pinned=PinnedType.IS_PINNED.value, pinned_start_datetime=now-datetime.timedelta(days=2),
                      pinned_end_datetime=now-datetime.timedelta(days=1), category=category2)
    # 置頂最新消息，仍在指定的置頂時間內，但無法顯示
    news5 = NewsModel(id=5, title='置頂時間正常但不可顯示的最新消息', content='只有後台看得到', group_id=7,
                      is_pinned=PinnedType.IS_PINNED.value, pinned_start_datetime=now,
                      pinned_end_datetime=now+datetime.timedelta(days=1),
                      visible_start_datetime=now-datetime.timedelta(days=2),
                      display_datetime=now-datetime.timedelta(days=2),
                      visible_end_datetime=now-datetime.timedelta(days=1), category=category2)
    # 置頂最新消息，但置頂時間已超過，顯示時間也已超過
    news6 = NewsModel(id=6, title='超過置頂時間的置頂最新消息，且顯示時間已過', content='只有後台看得到', group_id=7,
                      is_pinned=PinnedType.IS_PINNED.value, pinned_start_datetime=now-datetime.timedelta(days=2),
                      pinned_end_datetime=now+datetime.timedelta(days=1),
                      visible_start_datetime=now-datetime.timedelta(days=2),
                      display_datetime=now-datetime.timedelta(days=2),
                      visible_end_datetime=now-datetime.timedelta(days=1), category=category2)
    # 預約未來才會顯示的最新消息
    news7 = NewsModel(id=7, title='未來才看得到的最新消息', content='未來才看得到', group_id=7,
                      visible_start_datetime=now+datetime.timedelta(days=30),
                      display_datetime=now+datetime.timedelta(days=30),
                      visible_end_datetime=now+datetime.timedelta(days=40), category=category2)
    session.add(news1)
    session.add(news2)
    session.add(news3)
    session.add(news4)
    session.add(news5)
    session.add(news6)
    session.add(news7)

    # 因為跑 initialize_db.py 預先建立了幾個 page，所以這邊測試的 page id 從 13 開始
    calendar_page = PageModel(id=13, title='學校行事曆', content='<iframe src="https://calendar.google.com/calendar/embed?src=mail.bjes.tp.edu.tw_p5np58k8dbekppa6utlb8pbkek%40group.calendar.google.com&ctz=Asia%2FTaipei" style="border: 0" width="100%" height="600" frameborder="0" scrolling="no"></iframe>')
    session.add(calendar_page)
    # 接續 initialize_db.py 建立的資料繼續建立測試資料
    calendar_navbar = NavbarModel(name='學校行事曆', page=calendar_page, order=6, type=int(NavbarType.LEAF_NODE), icon='bi-calendar-date', ancestor_id=3)
    session.add(calendar_navbar)

    theme_config = json.loads(session.query(ThemeConfigModel.value).filter_by(name='yascms2020').scalar())
    new_homepage_item = {
        'name': '行事曆',
        'type': int(HomepageItemType.PAGE),
        'params': {
            'id': 13  # 上面建立的 page id
        },
        'description': '學校行事曆'
    }
    theme_config['settings']['homepage_items_order']['value'].append(new_homepage_item)
    (session.query(ThemeConfigModel)
            .filter_by(name='yascms2020')
            .update({ThemeConfigModel.value: json.dumps(theme_config, ensure_ascii=False)}))

    session.commit()
