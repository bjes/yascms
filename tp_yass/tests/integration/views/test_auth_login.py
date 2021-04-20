from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPFound

from tp_yass.views import auth


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

    form = mocker.patch.object(auth, 'LoginForm')
    form.validate.return_value = False

    login_view = auth.LoginView(request)
    response = login_view.post()

    assert isinstance(response, dict)
    assert 'login_form' in response


def test_login_post_view_with_valid_form_data_should_login_successfully_with_valid_credential(pyramid_config,
                                                                                              init_db_session,
                                                                                              mocker):
    """驗證帳號密碼正確的流程"""

    # 預設的 DummyRequest 啥都沒有，要自己補 log 會需要的 client_addr
    request = DummyRequest()
    request.client_addr = '127.0.0.1'

    login_form = mocker.MagicMock()
    login_form.validate.return_value = True
    login_form.account.data = 'admin'
    login_form.password.data = 'admin4tp_yass'
    mocker.patch.object(auth, 'LoginForm', return_value=login_form)

    login_view = auth.LoginView(request)
    response = login_view.post()

    assert isinstance(response, HTTPFound)

