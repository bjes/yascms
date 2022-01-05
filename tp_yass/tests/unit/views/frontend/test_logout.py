from pyramid import testing
from pyramid.httpexceptions import HTTPFound

from tp_yass.views.frontend import logout


def test_logout_view_will_logout_user(pyramid_config, mocker):
    mocker.patch.object(logout.DAL, 'log_auth')
    request = testing.DummyRequest()
    request.session['user_id'] = 100
    request.session['auth_source'] = 'foo'
    request.client_addr = '127.0.0.1'

    logout_view = logout.LogoutView(request)
    response = logout_view.logout()

    logout.DAL.log_auth.assert_called_once()
    assert isinstance(response, HTTPFound)
