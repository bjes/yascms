from datetime import datetime, timedelta

import transaction

from tp_yass.dal import DAL
from tp_yass.tests.integration.conftest import init_test_data


def test_get_frontend_news_list_should_return_valid_news_list(init_db_session):
    init_test_data()

    news_list = DAL.get_frontend_news_list()

    # 測試資料中，只有 id 為 1, 3, 4 的最新消息可以在前台看到
    assert len(news_list) == 3
    for news in news_list:
        assert news.id in [1, 3, 4]


def test_get_backend_news_list_should_return_all_news_list(init_db_session):
    init_test_data()

    news_list = DAL.get_backend_news_list().all()

    # 測試資料中 7 筆最新消息都應該在後台可以看到
    assert len(news_list) == 7


def test_get_page_quantity_of_total_news_should_return_page_quantity(init_db_session):
    init_test_data()

    # 測試資料總共 7 筆最新消息，若一頁一筆，可以分成 7 頁
    assert DAL.get_page_quantity_of_total_news(quantity_per_page=1, unpinned_only=False) == 7

    # 同上，但只算沒有設定置頂或置頂超過時間的最新消息總頁數
    assert DAL.get_page_quantity_of_total_news(quantity_per_page=1, unpinned_only=True) == 3


def test_get_frontend_news_should_return_news_if_visible(init_db_session):
    init_test_data()

    # 測試資料中 id 為 1 的最新消息，前台可以看
    assert DAL.get_frontend_news(1)

    # 測試資料中 id 為 2 的最新消息，前台不能看，因為已經超過顯示時間
    assert DAL.get_frontend_news(2) is None

    # 測試資料中 id 為 7 的最新消息顯示時間還沒到所以不能看
    news_id = 7
    assert DAL.get_frontend_news(news_id) is None
    news = DAL.get_news(news_id)
    # 將可顯示時間設定成昨天，也就是變成前台看得到
    news.visible_start_datetime = datetime.now() - timedelta(days=1)
    with transaction.manager:
        DAL.save_news(news)
    assert DAL.get_frontend_news(news_id)
    frontend_news_list = DAL.get_frontend_news_list()
    # 因為把 visible 設成昨天，所以應該會變成最後一筆最新消息（其他的最新消息都是以今天的日期建立）
    assert frontend_news_list[-1].id == news_id
