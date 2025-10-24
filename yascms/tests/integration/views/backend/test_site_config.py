from pyramid.testing import DummyRequest


def test_site_config_view(webtest_admin_testapp):
    """測試更新站台設定"""
    request = DummyRequest()

    response = webtest_admin_testapp.get(request.route_path('backend_site_config_edit'))
    assert response.status_int == 200
    assert '網站設定' in response.body.decode('utf8')

    # 無異動
    form = response.form
    response = form.submit()
    assert response.status_int == 200
    assert '網站設定無異動' in response.body.decode('utf8')

    # 錯誤格式
    response = webtest_admin_testapp.get(request.route_path('backend_site_config_edit'))
    form = response.form
    form['site_zip'] = 'foo'
    response = form.submit()
    assert response.status_int == 200
    assert '系統設定 site_zip 其值 foo 不合法，必須為整數' in response.body.decode('utf8')

    # 成功修改
    changed_name = 'foo_site_name'
    response = webtest_admin_testapp.get(request.route_path('backend_site_config_edit'))
    form = response.form
    form['site_name'] = changed_name
    response = form.submit()
    assert response.status_int == 302
    response = webtest_admin_testapp.get(request.route_path('backend_site_config_edit'))
    assert changed_name in response.body.decode('utf8')

