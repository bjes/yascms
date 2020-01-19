from pyramid.view import view_config
from tp_yass.dal import DAL


@view_config(route_name='index', renderer='themes/default/frontend/homepage.jinja2')
def homepage_view(request):
    return {'news': DAL.get_news_list()}
