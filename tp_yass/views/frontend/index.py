from pyramid.view import view_config


@view_config(route_name='index', renderer='themes/default/frontend/index.jinja2')
def index_view(request):
    return {'project': 'tp_yass'}
