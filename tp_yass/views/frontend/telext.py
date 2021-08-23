from pyramid.view import view_config

from tp_yass.enum import NavbarType
from tp_yass.helpers.navbar import generate_navbar_trees
from tp_yass.dal import DAL


@view_config(route_name='telext', renderer='')
def telext_view(request):
    request.override_renderer = f'themes/{request.current_theme_name}/frontend/telext.jinja2'
    return {'navbar_trees': generate_navbar_trees(request, visible_only=True),
            'NavbarType': NavbarType,
            'telext_list': DAL.get_pinned_telext_list()}
