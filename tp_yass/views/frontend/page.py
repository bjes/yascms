from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

from tp_yass.enum import NavbarType
from tp_yass.helpers.navbar import generate_navbar_trees
from tp_yass.dal import DAL


@view_config(route_name='page_get', renderer='tp_yass:themes/default/frontend/page_get.jinja2')
def page_get_view(request):
    page = DAL.get_page(request.matchdict['page_id'])
    if page:
        return {'navbar_trees': generate_navbar_trees(request, visible_only=True),
                'page': page,
                'NavbarType': NavbarType}
    else:
        return HTTPNotFound()
