from pyramid.testing import DummyRequest


def test_homepage_view_should_return_list(webtest_admin_testapp):
    request = DummyRequest()
    response = webtest_admin_testapp.get(request.route_path('backend_homepage'))
    assert '管理者' in response.body.decode('utf8')
