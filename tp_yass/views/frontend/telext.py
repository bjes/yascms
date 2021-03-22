from pyramid.view import view_config

from tp_yass.enum import NavbarType
from tp_yass.views.helper.navbar import generate_navbar_trees
from tp_yass.dal import DAL


@view_config(route_name='telext', renderer='tp_yass:themes/default/frontend/telext.jinja2')
def telext_view(request):
    return {'navbar_trees': generate_navbar_trees(request, visible_only=True),
            'NavbarType': NavbarType,
            'telext_list': DAL.get_pinned_telext_list()}
