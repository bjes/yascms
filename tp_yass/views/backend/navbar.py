from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound

from tp_yass.views.helper.navbar import generate_navbar_trees
from tp_yass.forms.backend.navbar import NavbarForm
from tp_yass.dal import DAL


@view_config(route_name='backend_navbar_list',
             renderer='themes/default/backend/navbar_list.jinja2',
             permission='view')
def backend_navbar_list_view(request):
    """後台顯示 navbar 樹狀結構"""
    return {'navbar_trees': generate_navbar_trees()}


@view_defaults(route_name='backend_navbar_create',
               renderer='themes/default/backend/navbar_create.jinja2',
               permission='edit')
class NavbarCreateView:
    """建立巢狀選單"""

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get_view(self):
        form = NavbarForm()
        return {'form': form, 'navbar_trees': generate_navbar_trees(type='intermediate')}

    @view_config(request_method='POST')
    def post_view(self):
        form = NavbarForm(self.request.POST)
        if form.validate():
            if DAL.create_navbar(form):
                return HTTPFound(self.request.route_url('backend_navbar_list'))
        return {'form': form, 'navbar_trees': generate_navbar_trees(type='intermediate')}

