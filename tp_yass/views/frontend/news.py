from pyramid.view import view_config

from tp_yass.views.helper.navbar import generate_navbar_trees
from tp_yass.dal import DAL


def _sanitize_input(param, param_type, default_value):
    """正規化從 GET 傳入的參數

    Args:
        param: 傳入的參數值
        param_type: 該參數應該是什麼類型，比方 int
        default_value: 若無法轉型成 param_type，預設回傳值

    Returns:
        回傳正規化後的值
    """
    try:
        return param_type(param)
    except:
        return default_value

@view_config(route_name='news_list', renderer='tp_yass:themes/default/frontend/news_list.jinja2')
def news_list_view(request):
    quantity_per_page = _sanitize_input(request.GET.get('q', 20), int, 20)
    category_id = _sanitize_input(request.GET.get('c', None), int, None)
    page_id = _sanitize_input(request.GET.get('p', 1), int, 1)
    news_list = DAL.get_news_list(page=page_id, category_id=category_id, quantity_per_page=quantity_per_page)
    return {'news_list': news_list,
            'navbar_trees': generate_navbar_trees(DAL.get_navbar_list()),
            'page_quantity_of_total_news': DAL.get_page_quantity_of_total_news(quantity_per_page, category_id),
            'page_id': page_id,
            'quantity_per_page': quantity_per_page}
