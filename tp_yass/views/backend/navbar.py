from pyramid.view import view_config

from tp_yass.dal import DAL
from tp_yass.views.helper.navbar import generate_navbar_trees


@view_config(route_name='backend_navbar_list',
             renderer='themes/default/backend/navbar_list.jinja2',
             permission='view')
def backend_navbar_list_view(request):
    return {'navbar_trees': generate_navbar_trees(DAL.get_navbar_list())}
