from pyramid.testing import DummyRequest


def test_news_list_should_return_viewable_news(webtest_testapp):
    request = DummyRequest()

    response = webtest_testapp.get(request.route_path('news_list'))
    assert response.status_int == 200
    # 前台可以看得到的測試最新消息只有 3 組，加上標題共 4 組 <tr>
    assert response.body.decode('utf8').count('<tr>') == 4

