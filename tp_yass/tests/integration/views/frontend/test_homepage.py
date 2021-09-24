from pyramid.testing import DummyRequest


def test_homepage(webtest_testapp, pyramid_config):
    request = DummyRequest()
    response = webtest_testapp.get(request.route_path('homepage'))
    assert response.status_int == 200
