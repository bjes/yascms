import plaster
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker


def get_ini_settings(ini_file_path):
    """Return ini settings"""

    return plaster.get_settings(ini_file_path, 'app:main')


def import_test_db_data(ini_file_path):
    """Import test data to test database"""
    from tp_yass.models.user import GroupModel, UserModel
    from tp_yass.models.news import NewsModel, NewsCategoryModel
    from tp_yass.models.sys_config import SysConfigModel

    ini_settings = get_ini_settings(ini_file_path)
    engine = engine_from_config(ini_settings)
    Session = sessionmaker(bind=engine)

    session = Session()

    # 初始化系統設定
    session.query(SysConfigModel).filter_by(name='site_name').update({'value': '臺北市中山區濱江國小'})
    session.query(SysConfigModel).filter_by(name='site_slogan').update({'value': '快樂學習 - 教學相長'})
    session.query(SysConfigModel).filter_by(name='site_theme').update({'value': 'tp_yass'})
    session.query(SysConfigModel).filter_by(name='site_phone').update({'value': '02-85021571'})
    session.query(SysConfigModel).filter_by(name='site_fox').update({'value': '02-85011146'})
    session.query(SysConfigModel).filter_by(name='site_email').update({'value': 'public@bjes.tp.edu.tw'})
    session.query(SysConfigModel).filter_by(name='site_zip').update({'value': '10462'})
    session.query(SysConfigModel).filter_by(name='site_address').update({'value': '臺北市中山區樂群二路266巷99號'})
    session.query(SysConfigModel).filter_by(name='site_google_map_url').update({'value': 'https://goo.gl/maps/X6Y4E37U66aMqQHY6'})
    session.query(SysConfigModel).filter_by(name='site_google_map_embedded_url').update({'value': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3613.7043991522146!2d121.55944821523249!3d25.07800624267944!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3442ac72e5e39d17%3A0x3934b7c47c1bbf29!2zMTA0OTHlj7DljJfluILkuK3lsbHljYDmqILnvqTkuozot68yNjblt7c5OeiZnw!5e0!3m2!1szh-TW!2stw!4v1551164410802'})
    session.query(SysConfigModel).filter_by(name='site_google_calendar_embedded_url').update({'value': 'https://calendar.google.com/calendar/embed?src=mail.bjes.tp.edu.tw_p5np58k8dbekppa6utlb8pbkek%40group.calendar.google.com&ctz=Asia%2FTaipei'})
    session.commit()

    # 建群組。初始化資料庫時會先建立 admin (所以其 id 為 1) 這邊從 2 開始
    group1 = GroupModel(id=2, name='測試國小', type=1)
    group2 = GroupModel(id=3, name='教務處', type=1, ancestor_id=2)
    group3 = GroupModel(id=4, name='自然領域科任', type=1, ancestor_id=2)
    group4 = GroupModel(id=5, name='藝文領域科任', type=1, ancestor_id=2)
    group5 = GroupModel(id=6, name='資訊組', type=1, ancestor_id=3)
    group6 = GroupModel(id=7, name='系管師', type=1, ancestor_id=3)
    # 建帳號。初始化資料庫時會先建立 admin (所以其 id 為 1) 這邊從 2 開始
    user1 = UserModel(id=2, first_name='陳', last_name='小明', email='user1@xxx.tp.edu.tw',
                      account='user1', password='user1', status=1)
    # user1 群組為資訊組、藝文領域科任
    user1.groups = [group5, group4]
    user2 = UserModel(id=3, first_name='王', last_name='大寶', email='user2@xxx.tp.edu.tw',
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
    # 建最新消息
    news1 = NewsModel(id=1, title='採購 10 台伺服器', content='設備已放機房', group_id=6, category=category1)
    news2 = NewsModel(id=2, title='暑假第一天將重灌電腦', content='請老師及早備份資料', group_id=7, is_pinned=1, category=category2)
    session.add(news1)
    session.add(news2)

    session.commit()
