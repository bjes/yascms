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

    ini_settings = get_ini_settings(ini_file_path)
    engine = engine_from_config(ini_settings)
    Session = sessionmaker(bind=engine)

    session = Session()

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
    user1.groups = [group5, group4]
    user2 = UserModel(id=3, first_name='王', last_name='大寶', email='user2@xxx.tp.edu.tw',
                      account='user2', password='user2', status=1)
    user2.groups = [group6, group3]

    # 建最新消息分類群組
    category1 = NewsCategoryModel(id=1, name='行政公告')
    category2 = NewsCategoryModel(id=2, name='學校榮譽')

    # 建最新消息
    news1 = NewsModel(id=1, title='採購 10 台伺服器', content='設備已放機房', group_id=6, category_id=1)
    news2 = NewsModel(id=2, title='暑假第一天將重灌電腦', content='請老師及早備份資料', group_id=7, is_pinned=1, category_id=2)

    session.add(group1)
    session.add(group2)
    session.add(group3)
    session.add(group4)
    session.add(group5)
    session.add(group6)
    session.add(user1)
    session.add(user2)
    session.add(category1)
    session.add(category2)
    session.add(news1)
    session.add(news2)

    session.commit()
