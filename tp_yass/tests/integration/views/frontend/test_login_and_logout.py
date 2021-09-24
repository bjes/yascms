from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPFound

from tp_yass.views.frontend import login


def test_login_logic(webtest_testapp, pyramid_config):
    """直接用 webtest 去測試是否能登入網站"""
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


def test_login_post_view_with_invalid_form_data_should_return_list_with_login_form(pyramid_config,
                                                                                   init_db_session,
                                                                                   mocker):
    """測試表單驗證失敗的行為"""
    request = DummyRequest()
    request.current_theme_name = 'tp_yass2020'

    form = mocker.patch.object(login, 'LoginForm')
    form.validate.return_value = False

    login_view = login.LoginView(request)
    response = login_view.post()

    assert isinstance(response, dict)
    assert 'login_form' in response


def test_login_post_view_with_valid_form_data_should_login_successfully_with_valid_credential(pyramid_config,
                                                                                              init_db_session,
                                                                                              mocker):
    """驗證帳號密碼正確的流程"""

    # 預設的 DummyRequest 啥都沒有，要自己補 log 會需要的 client_addr
    request = DummyRequest()
    request.current_theme_name = 'tp_yass2020'
    request.client_addr = '127.0.0.1'

    # 驗證最高權限的帳號登入的行為
    login_form = mocker.MagicMock()
    login_form.validate.return_value = True
    login_form.account.data = 'admin'
    login_form.password.data = 'admin4tp_yass'
    mocker.patch.object(login, 'LoginForm', return_value=login_form)

    login_view = login.LoginView(request)
    response = login_view.post()

    assert login_view.request.session['is_admin']
    # 在測試資料中，最高管理者群組其 id 為 2
    assert login_view.request.session['main_group_id_list'] == {2}
    assert login_view.request.session['groups'] == [[{'name': '最高管理者群組', 'id': 2, 'type': 0},
                                                     {'name': '根群組', 'id': 1, 'type': 2}]]
    assert login_view.request.session['group_id_list'] == {1, 2}
    assert isinstance(response, HTTPFound)

    # 驗證一般使用者的帳號登入行為
    login_form = mocker.MagicMock()
    login_form.validate.return_value = True
    login_form.account.data = 'user1'
    login_form.password.data = 'user1'
    mocker.patch.object(login, 'LoginForm', return_value=login_form)

    login_view = login.LoginView(request)
    response = login_view.post()

    assert login_view.request.session['is_admin'] == False
    assert login_view.request.session['main_group_id_list'] == {6, 7}
    assert login_view.request.session['groups'] == [[{'name': '藝文領域科任', 'id': 6, 'type': 2},
                                                     {'name': '測試國小', 'id': 3, 'type': 2},
                                                     {'name': '根群組', 'id': 1, 'type': 2}],
                                                    [{'name': '資訊組', 'id': 7, 'type': 1},
                                                     {'name': '教務處', 'id': 4, 'type': 1},
                                                     {'name': '測試國小', 'id': 3, 'type': 2},
                                                     {'name': '根群組', 'id': 1, 'type': 2}]]
    assert login_view.request.session['group_id_list'] == {1, 3, 4, 6, 7}
    assert isinstance(response, HTTPFound)


def test_login_and_logout_logic_with_via_webtest(webtest_testapp):
    request = DummyRequest()

    response = webtest_testapp.get(request.route_url('backend_homepage'), expect_errors=True)
    assert response.status_int == 403

    # 一般使用者
    response = webtest_testapp.get(request.route_url('login'))
    form = response.form
    form['account'] = 'user1'
    form['password'] = 'user1'
    form.submit()
    response = webtest_testapp.get(request.route_url('backend_homepage'))
    assert response.status_int == 200
    response = webtest_testapp.get(request.route_url('backend_site_config_edit'), expect_errors=True)
    assert response.status_int == 403
    webtest_testapp.get(request.route_url('logout'))
    response = webtest_testapp.get(request.route_url('backend_homepage'), expect_errors=True)
    assert response.status_int == 403

    # 管理者
    response = webtest_testapp.get(request.route_url('login'))
    form = response.form
    form['account'] = 'admin'
    form['password'] = 'admin4tp_yass'
    form.submit()
    response = webtest_testapp.get(request.route_url('backend_homepage'))
    assert response.status_int == 200
    response = webtest_testapp.get(request.route_url('backend_site_config_edit'), expect_errors=True)
    assert response.status_int == 200
    webtest_testapp.get(request.route_url('logout'))
    response = webtest_testapp.get(request.route_url('backend_homepage'), expect_errors=True)
    assert response.status_int == 403
