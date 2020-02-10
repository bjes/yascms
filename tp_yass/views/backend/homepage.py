from pyramid.view import view_config


@view_config(route_name='backend_homepage', renderer='themes/default/backend/homepage.jinja2', permission='view')
def backend_homepage_view(request):
    return {}
