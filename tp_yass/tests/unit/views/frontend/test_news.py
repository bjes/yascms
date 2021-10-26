from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPNotFound

from tp_yass.views.frontend import news


def test_news_list_view_should_return_dict(mocker):
    mocker.patch.object(news.DAL, 'get_news_list')
    mocker.patch.object(news.DAL, 'get_news_category')
    mocker.patch.object(news.DAL, 'get_page_quantity_of_total_news')
    mocker.patch.object(news, 'generate_navbar_trees')
    request = DummyRequest()
    request.current_theme_name = request.effective_theme_name = 'tp_yass2020'
    response = news.news_list_view(request)
    valid_keys = ['news_list', 'news_category', 'navbar_trees',
                  'page_quantity_of_total_news', 'page_number',
                  'quantity_per_page', 'NavbarType']
    for key in valid_keys:
        assert key in response


def test_news_get_view_should_return_news_info(mocker):
    mocker.patch.object(news.DAL, 'get_news')
    mocker.patch.object(news, 'generate_navbar_trees')
    request = DummyRequest()
    request.current_theme_name = request.effective_theme_name = 'tp_yass2020'
    request.matchdict['news_id'] = '999'

    # 若資料庫有對應的 news 物件
    response = news.news_get_view(request)
    assert isinstance(response, dict)
    valid_keys = ['navbar_trees', 'NavbarType', 'news']
    for key in valid_keys:
        assert key in response

    # 若資料庫沒有對應的 news 物件要回傳 http not found
    mocker.patch.object(news.DAL, 'get_news', return_value=None)
    response = news.news_get_view(request)
    assert isinstance(response, HTTPNotFound)
