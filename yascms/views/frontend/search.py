import datetime

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

from yascms.enum import NavbarType
from yascms.helpers.navbar import generate_navbar_trees
from yascms.dal import DAL


@view_config(route_name='search', renderer='')
def search_view(request):
    """前台顯示搜尋表單"""
    request.override_renderer = f'themes/{request.effective_theme_name}/frontend/search.jinja2'
    return {'navbar_trees': generate_navbar_trees(request, visible_only=True),
            'NavbarType': NavbarType}


@view_config(route_name='search_results', renderer='')
def search_results_view(request):
    """前台顯示搜尋結果"""
    request.override_renderer = f'themes/{request.effective_theme_name}/frontend/search_results.jinja2'
    try:
        key   = request.GET['key']
        value = request.GET['value']
        if key not in ('publisher', 'title', 'content'):
            return HTTPNotFound()
        if value.strip() == '':
            return HTTPNotFound()

        results = DAL.get_search_results(key, value)
        return {'navbar_trees': generate_navbar_trees(request, visible_only=True),
                'NavbarType': NavbarType,
                'results': results}
    except KeyError:
        return HTTPNotFound()

