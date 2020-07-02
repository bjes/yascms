from pyramid.view import view_config

from tp_yass.views.helper.navbar import generate_navbar_trees
from tp_yass.views.frontend.helper import remove_navbar_root
from tp_yass.dal import DAL


@view_config(route_name='homepage', renderer='themes/default/frontend/homepage.jinja2')
def homepage_view(request):
    return {'news_list': DAL.get_latest_news(int(request.sys_config['site_homepage_news_quantity'])),
            'navbar_trees': remove_navbar_root(generate_navbar_trees(request, visible_only=True)),
            'telext_list': DAL.get_pinned_telext_list(),
            'link_list': DAL.get_pinned_link_list()}
