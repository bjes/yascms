from pyramid.view import view_config


@view_config(route_name='index', renderer='themes/default/frontend/index.jinja2')
def index_view(request):
    return {'project': 'tp_yass'}

@view_config(route_name='login', renderer='themes/default/frontend/login.jinja2')
def login_view(request):
    return {}
