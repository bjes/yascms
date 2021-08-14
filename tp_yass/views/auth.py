import logging

from pyramid.view import view_config
from pyramid.security import forget
from pyramid.httpexceptions import HTTPFound

from tp_yass.enum import AuthLogType
from tp_yass.dal import DAL


logger = logging.getLogger(__name__)


class LogoutView:

    def __init__(self, request):
        self.request = request

    @view_config(route_name='logout')
    def logout(self):
        DAL.log_auth(AuthLogType.LOGOUT, self.request.session['user_id'], self.request.client_addr)
        headers = forget(self.request)
        self.request.session.clear()
        return HTTPFound(location=self.request.route_url('homepage'),
                         headers=headers)
