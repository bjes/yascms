from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

from tp_yass.enum import NavbarType
from tp_yass.helpers import sanitize_input
from tp_yass.helpers.navbar import generate_navbar_trees
from tp_yass.dal import DAL


@view_config(route_name='news_list', renderer='tp_yass:themes/default/frontend/news_list.jinja2')
def news_list_view(request):
    """前台顯示最新消息列表"""
    quantity_per_page = sanitize_input(request.GET.get('q', 20), int, 20)
    category_id = sanitize_input(request.GET.get('c'), int, None)
    page_number = sanitize_input(request.GET.get('p', 1), int, 1)

    news_list = DAL.get_news_list(page_number=page_number, category_id=category_id, quantity_per_page=quantity_per_page)
    return {'news_list': news_list,
            'news_category': DAL.get_news_category(category_id),
            'navbar_trees': generate_navbar_trees(request, visible_only=True),
            'page_quantity_of_total_news': DAL.get_page_quantity_of_total_news(quantity_per_page, category_id),
            'page_number': page_number,
            'quantity_per_page': quantity_per_page,
            'NavbarType': NavbarType}


@view_config(route_name='news_get', renderer='tp_yass:themes/default/frontend/news_get.jinja2')
def news_get_view(request):
    """前台顯示單一最新消息"""
    news_id = int(request.matchdict['news_id'])
    news = DAL.get_news(news_id)
    if news:
        return {'navbar_trees': generate_navbar_trees(request, visible_only=True),
                'NavbarType': NavbarType,
                'news': news}
    else:
        return HTTPNotFound()
