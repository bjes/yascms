from pyramid.testing import DummyRequest


def test_theme_list(webtest_admin_testapp):
    request = DummyRequest()

    response = webtest_admin_testapp.get(request.route_path('backend_theme_list'))
    assert response.status_int == 200
    assert 'tp_yass2020' in response.body.decode('utf8')


def test_theme_config_general_edit_view(webtest_admin_testapp):
    request = DummyRequest()

    response = webtest_admin_testapp.get(request.route_path('backend_theme_config_general_edit',
                                                            theme_name='tp_yass2020'))
    assert response.status_int == 200
    assert '一般設定' in response.body.decode('utf8')

    form = response.form
    # 會 redirect 回 request.route_url('backend_theme_list')
    response = form.submit()
    assert response.status_int == 302
    assert 'backend/theme/list' in response.location
