from pyramid import testing
from pyramid.httpexceptions import HTTPFound

from tp_yass.views import auth


def test_logout_logout_view_will_logout_user(pyramid_config, mocker):
    mocker.patch.object(auth.DAL, 'log_auth')
    request = testing.DummyRequest()
    request.session['user_id'] = 100
    request.client_addr = '127.0.0.1'

    logout_view = auth.LogoutView(request)
    response = logout_view.logout()

    auth.DAL.log_auth.assert_called_once()
    assert isinstance(response, HTTPFound)
