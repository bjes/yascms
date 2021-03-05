from pyramid.testing import DummyRequest

from tp_yass.views.backend import api
from tp_yass.models.page import PageModel


def test_backend_api_page_list_view_should_return_page_list(pyramid_config, mocker):
    mimic_page_list = [PageModel(id=1, title='foo'), PageModel(id=2, title='bar')]
    mocker.patch.object(api.DAL, 'get_page_list', return_value=mimic_page_list)

    response = api.backend_api_page_list_view(DummyRequest())
    assert len(response) == len(mimic_page_list)
    valid_keys = ['id', 'title', 'url']
    for page in response:
        for key in valid_keys:
            assert key in page


def test_backend_api_page_get_view_should_return_page(pyramid_config, mocker):
    request = DummyRequest()
    request.matchdict['page_id'] = '999'

    # 模擬資料庫有 page 物件
    mocker.patch.object(api.DAL, 'get_page')
    response = api.backend_api_page_get_view(request)
    valid_keys = ['id', 'title', 'url']
    for key in valid_keys:
        assert key in response

    # 模擬資料庫若沒有物件則回傳空的 list
    mocker.patch.object(api.DAL, 'get_page', return_value=None)
    response = api.backend_api_page_get_view(request)
    assert response == {}
