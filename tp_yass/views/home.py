from pyramid.view import view_config


@view_config(route_name='home', renderer='themes/default/home.jinja2')
def home_view(request):
    return {'project': 'tp_yass'}

