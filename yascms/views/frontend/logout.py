import logging

from pyramid.view import view_config
from pyramid.security import forget
from pyramid.httpexceptions import HTTPFound

from yascms.enum import AuthLogType
from yascms.dal import DAL


logger = logging.getLogger(__name__)


class LogoutView:

    def __init__(self, request):
        self.request = request

    @view_config(route_name='logout')
    def logout(self):
        DAL.log_auth(AuthLogType.LOGOUT, self.request.session['user_id'],
                     self.request.client_addr, self.request.session['auth_source'])
        headers = forget(self.request)
        self.request.session.clear()
        return HTTPFound(location=self.request.route_url('homepage'),
                         headers=headers)
