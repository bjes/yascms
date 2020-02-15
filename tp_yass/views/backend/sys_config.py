from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound

from tp_yass.forms.backend.sys_config import SysConfigEntryForm, SysConfigForm
from tp_yass.dal import DAL


@view_defaults(route_name='backend_sys_config_edit', renderer='tp_yass:themes/default/backend/sys_config_edit.jinja2')
class SysConfigView:

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def list_view(self):
        sys_config_form = SysConfigForm()
        for config in DAL.get_sys_config_list():
            sys_config_form.config.append_entry(SysConfigEntryForm(name=config.name, value=config.value, description=config.description))
        return {'sys_config_form': sys_config_form}

    @view_config(request_method='POST')
    def post_view(self):
        sys_config_form = SysConfigForm(self.request.POST)
        if sys_config_form.validate():
            print('oops')
            return HTTPFound(location=self.request.route_url('backend_homepage'))
        else:
            print('ohhhhhhhh')
            return HTTPFound(location=self.request.route_url('backend_homepage'))
