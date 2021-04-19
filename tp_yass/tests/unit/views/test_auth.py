from pyramid import testing
from pyramid.httpexceptions import HTTPFound

from tp_yass.views import auth


def test_login_get_view_with_logged_in_state_should_return_httpfound_backend_url(pyramid_config):
    request = testing.DummyRequest()
    request.session['account'] = 'foo'
    login_view = auth.LoginView(request)
    response = login_view.get()
    assert isinstance(response, HTTPFound)


def test_login_get_view_with_anonymous_should_return_login_form(pyramid_config):
    request = testing.DummyRequest()
    login_view = auth.LoginView(request)
    response = login_view.get()
    assert 'login_form' in response


def test_logout_logout_view_will_logout_user(pyramid_config, mocker):
    mocker.patch.object(auth.DAL, 'log_auth')
    request = testing.DummyRequest()
    request.session['user_id'] = 100
    request.client_addr = '127.0.0.1'

    logout_view = auth.LogoutView(request)
    response = logout_view.logout()

    auth.DAL.log_auth.assert_called_once()
    assert isinstance(response, HTTPFound)
