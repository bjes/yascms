from pyramid.view import view_config

from tp_yass.helper import sanitize_input
from tp_yass.views.helper.navbar import generate_navbar_trees
from tp_yass.dal import DAL


@view_config(route_name='news_list', renderer='tp_yass:themes/default/frontend/news_list.jinja2')
def news_list_view(request):
    quantity_per_page = sanitize_input(request.GET.get('q', 20), int, 20)
    category_id = sanitize_input(request.GET.get('c'), int, None)
    page_id = sanitize_input(request.GET.get('p', 1), int, 1)
    news_list = DAL.get_news_list(page=page_id, category_id=category_id, quantity_per_page=quantity_per_page)
    return {'news_list': news_list,
            'navbar_trees': generate_navbar_trees(DAL.get_navbar_list()),
            'page_quantity_of_total_news': DAL.get_page_quantity_of_total_news(quantity_per_page, category_id),
            'page_id': page_id,
            'quantity_per_page': quantity_per_page}
