from pyramid import testing
from pyramid.httpexceptions import HTTPFound

from tp_yass.views.frontend import login


def test_login_get_view_with_logged_in_state_should_return_httpfound_backend_url(pyramid_config):
    request = testing.DummyRequest()
    request.current_theme = 'tp_yass2020'
    request.session['account'] = 'foo'
    login_view = login.LoginView(request)
    response = login_view.get()
    assert isinstance(response, HTTPFound)


def test_login_get_view_with_anonymous_should_return_login_form(pyramid_config):
    request = testing.DummyRequest()
    request.current_theme = 'tp_yass2020'
    login_view = login.LoginView(request)
    response = login_view.get()
    assert 'login_form' in response
