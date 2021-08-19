from pyramid.view import view_config

from tp_yass.enum import NavbarType
from tp_yass.helpers.navbar import generate_navbar_trees
from tp_yass.dal import DAL


@view_config(route_name='homepage', renderer='')
def homepage_view(request):
    request.override_renderer = f'themes/{request.current_theme}/frontend/homepage.jinja2'
    return {'news_list': DAL.get_latest_news(int(request.site_config['site_homepage_news_quantity'])),
            'navbar_trees': generate_navbar_trees(request, visible_only=True),
            'telext_list': DAL.get_pinned_telext_list(),
            'link_list': DAL.get_pinned_link_list(),
            'NavbarType': NavbarType}
