from pyramid.testing import DummyRequest


def test_login_logic(webtest_testapp, pyramid_config):
    request = DummyRequest()
    response = webtest_testapp.get(request.route_path('backend_homepage'), expect_errors=True)
    assert response.status_int == 403

    response = webtest_testapp.get(request.route_path('login'))
    form = response.form
    form['account'] = 'wrong_account'
    form['password'] = 'wrong_password'
    response = form.submit()
    assert '登入失敗' in response.body.decode('utf8')

    response = webtest_testapp.get(request.route_path('login'))
    form = response.form
    form['account'] = 'admin'
    form['password'] = 'admin4tp_yass'
    form.submit()
    response = webtest_testapp.get(request.route_path('backend_homepage'))
    assert '管理者' in response.body.decode('utf8')
