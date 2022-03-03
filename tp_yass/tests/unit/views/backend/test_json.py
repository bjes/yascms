from pyramid.testing import DummyRequest

from tp_yass.views.backend import json
from tp_yass.models.page import PageModel


def test_backend_json_page_list_view_should_return_page_list(pyramid_config, mocker):
    fake_page_list = [PageModel(id=1, title='foo'), PageModel(id=2, title='bar')]
    mocker.patch.object(json.DAL, 'get_page_list', return_value=fake_page_list)

    response = json.backend_json_page_list_view(DummyRequest())
    assert len(response) == len(fake_page_list)
    valid_keys = ['id', 'title', 'url']
    for page in response:
        for key in valid_keys:
            assert key in page


def test_backend_json_page_get_view_should_return_page(pyramid_config, mocker):
    request = DummyRequest()
    request.matchdict['page_id'] = '999'

    # 模擬資料庫有 page 物件
    mocker.patch.object(json.DAL, 'get_page')
    response = json.backend_json_page_get_view(request)
    valid_keys = ['id', 'title', 'url']
    for key in valid_keys:
        assert key in response

    # 模擬資料庫若沒有物件則回傳空的 list
    mocker.patch.object(json.DAL, 'get_page', return_value=None)
    response = json.backend_json_page_get_view(request)
    assert response == {}
