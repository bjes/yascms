from pyramid.view import view_config


@view_config(route_name='backend_homepage', renderer='', permission='view')
def backend_homepage_view(request):
    request.override_renderer = f'themes/{request.current_theme}/backend/homepage.jinja2'
    return {}
