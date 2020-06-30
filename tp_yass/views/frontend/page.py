from pyramid.view import view_config

from tp_yass.views.helper.navbar import generate_navbar_trees
from tp_yass.dal import DAL


@view_config(route_name='page_get', renderer='tp_yass:themes/default/frontend/page_get.jinja2')
def page_get_view(request):
    page = DAL.get_page(request.matchdict['page_id'])
    return {'navbar_trees': generate_navbar_trees(request), 'page': page}
