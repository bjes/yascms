from pyramid.view import view_config
from tp_yass.dal import DAL


@view_config(route_name='index', renderer='themes/default/frontend/index.jinja2')
def index_view(request):
    return {'news': DAL.get_news_list()}
