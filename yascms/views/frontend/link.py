from pyramid.view import view_config

from yascms.enum import NavbarType
from yascms.helpers.navbar import generate_navbar_trees
from yascms.dal import DAL


@view_config(route_name='links', renderer='')
def links_view(request):
    request.override_renderer = f'themes/{request.effective_theme_name}/frontend/links.jinja2'
    return {'navbar_trees': generate_navbar_trees(request, visible_only=True),
            'NavbarType': NavbarType,
            'link_category_list': DAL.get_link_category_list()}
