from pyramid.view import view_config

from tp_yass.enum import NavbarType
from tp_yass.views.helper.navbar import generate_navbar_trees


@view_config(route_name='calendar', renderer='tp_yass:themes/default/frontend/calendar.jinja2')
def calendar_view(request):
    return {'navbar_trees': generate_navbar_trees(request, visible_only=True),
            'NavbarType': NavbarType}
