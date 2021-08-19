from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPNotFound

from tp_yass.views.frontend import page


def test_page_get_view_should_return_dict(mocker):
    mocker.patch.object(page.DAL, 'get_page')
    mocker.patch.object(page, 'generate_navbar_trees')
    request = DummyRequest()
    request.current_theme = 'tp_yass2020'
    request.matchdict['page_id'] = '999'

    # 模擬有對應的 page 物件於資料庫
    response = page.page_get_view(request)
    valid_keys = ['navbar_trees', 'page', 'NavbarType']
    for key in valid_keys:
        assert key in response

    # 模擬資料庫沒這筆資料
    mocker.patch.object(page.DAL, 'get_page', return_value=None)
    response = page.page_get_view(request)
    assert isinstance(response, HTTPNotFound)
