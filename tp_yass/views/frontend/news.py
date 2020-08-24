from pyramid.view import view_config

from tp_yass.enum import NavbarType
from tp_yass.helper import sanitize_input
from tp_yass.views.helper.navbar import generate_navbar_trees
from tp_yass.views.frontend.helper import remove_navbar_root
from tp_yass.dal import DAL


@view_config(route_name='news_list', renderer='tp_yass:themes/default/frontend/news_list.jinja2')
def news_list_view(request):
    quantity_per_page = sanitize_input(request.GET.get('q', 20), int, 20)
    category_id = sanitize_input(request.GET.get('c'), int, None)
    page_number = sanitize_input(request.GET.get('p', 1), int, 1)
    news_list = DAL.get_news_list(page_number=page_number, category_id=category_id, quantity_per_page=quantity_per_page)
    return {'news_list': news_list,
            'navbar_trees': remove_navbar_root(generate_navbar_trees(request, visible_only=True)),
            'page_quantity_of_total_news': DAL.get_page_quantity_of_total_news(quantity_per_page, category_id),
            'page_number': page_number,
            'quantity_per_page': quantity_per_page,
            'NavbarType': NavbarType}
