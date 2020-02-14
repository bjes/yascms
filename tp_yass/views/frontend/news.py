import math

from pyramid.view import view_config

from tp_yass.dal import DAL


def _calculate_page_quantity(news_list, quantity_per_page):
    """計算最新消息總共產生的頁數"""
    return math.ceil(len(news_list)/quantity_per_page)


@view_config(route_name='news_list', renderer='tp_yass:themes/default/frontend/news_list.jinja2')
def news_list_view(request):
    news = DAL.get_news_list(category_id=request.GET.get('category_id', None),
                             quantity_per_page=int(request.sysconfig['homepage_news_quantity']))
    return {'news': news,
            'page_quantity': _calculate_page_quantity(news, int(request.sysconfig['homepage_news_quantity']))}
