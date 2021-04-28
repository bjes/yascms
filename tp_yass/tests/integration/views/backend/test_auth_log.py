from pyramid.testing import DummyRequest


def test_auth_log_list_view(webtest_admin_testapp):
    """webtest_admin_testapp 這個 fixture 本身就會產生一筆登入成功的紀錄，
    所以直接撈網頁確認有無該紀錄"""
    request = DummyRequest()

    response = webtest_admin_testapp.get(request.route_path('backend_auth_log_list'))
    assert response.status_int == 200
    assert '登入' in response.body.decode('utf8')
