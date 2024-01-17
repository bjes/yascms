from pyramid.testing import DummyRequest


def test_news_list_should_return_all_news(webtest_admin_testapp):
    request = DummyRequest()

    response = webtest_admin_testapp.get(request.route_path('backend_news_list'))
    assert response.status_int == 200
    # 最新消息有 7 筆，加上標題，一共 8 組 <tr>
    assert response.body.decode('utf8').count('<tr>') == 8

