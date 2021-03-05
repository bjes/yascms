from pyramid import testing
from pyramid.httpexceptions import HTTPFound

from tp_yass.views.auth import LoginView, LogoutView


def test_login_get_view_with_logged_in_state_should_return_httpfound_backend_url(pyramid_config):
    request = testing.DummyRequest()
    request.session['account'] = 'foo'
    login_view = LoginView(request)
    response = login_view.get()
    assert isinstance(response, HTTPFound)


def test_login_get_view_with_anonymous_should_return_login_form(pyramid_config):
    request = testing.DummyRequest()
    login_view = LoginView(request)
    response = login_view.get()
    assert 'login_form' in response


def test_logout_logout_view_will_logout_user(pyramid_config):
    request = testing.DummyRequest()
    request.session['account'] = 'foo'
    logout_view = LogoutView(request)
    response = logout_view.logout()
    assert isinstance(response, HTTPFound)
