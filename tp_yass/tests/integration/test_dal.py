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

    # 測試資料中 6 筆最新消息都應該在後台可以看到
    assert len(news_list) == 6


def test_get_page_quantity_of_total_news_should_return_page_quantity(init_db_session):
    init_test_data()

    # 測試資料總共 6 筆最新消息，若一頁一筆，可以分成 6 頁
    assert DAL.get_page_quantity_of_total_news(quantity_per_page=1, unpinned_only=False) == 6

    # 同上，但只算沒有設定置頂或置頂超過時間的最新消息總頁數
    assert DAL.get_page_quantity_of_total_news(quantity_per_page=1, unpinned_only=True) == 3

