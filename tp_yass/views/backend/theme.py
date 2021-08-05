import logging

from pyramid.view import view_config

from tp_yass.dal import DAL


logger = logging.getLogger(__name__)


@view_config(route_name='backend_theme_list',
             renderer='tp_yass:themes/default/backend/theme_list.jinja2',
             permission='view')
def theme_list_view(request):
    return {'theme_list': DAL.get_theme_list()}
