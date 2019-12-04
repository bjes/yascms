from pyramid.view import view_config, view_defaults

from ...schemas import


@view_defaults(route_name='login', renderer='themes/default/frontend/login.jinja2')
class LoginView:

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get(self):
        return {}

    @view_config(request_method='POST')
    def post(self):
        pass
