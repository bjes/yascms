from pyramid.view import view_config

from tp_yass.enum import NavbarType
from tp_yass.views.helper.navbar import generate_navbar_trees
from tp_yass.views.frontend.helper import remove_navbar_root
from tp_yass.dal import DAL


@view_config(route_name='links', renderer='tp_yass:themes/default/frontend/links.jinja2')
def links_view(request):
    return {'navbar_trees': remove_navbar_root(generate_navbar_trees(request, visible_only=True)),
            'NavbarType': NavbarType,
            'link_category_list': DAL.get_link_category_list()}
