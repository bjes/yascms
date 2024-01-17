from pyramid.view import view_config
from yascms.dal import DAL


@view_config(route_name='backend_json_page_list', renderer='json', permission='view')
def backend_json_page_list_view(request):
    """回傳單一頁面的列表 json"""
    page_list = []
    for each_page in DAL.get_page_list(pagination=False):
        page_list.append({'id': each_page.id,
                          'title': each_page.title,
                          'url': request.route_url('page_get', page_id=each_page.id)})
    return page_list


@view_config(route_name='backend_json_page_get', renderer='json', permission='view')
def backend_json_page_get_view(request):
    """回傳單一頁面的 json"""
    page = DAL.get_page(int(request.matchdict['page_id']))
    if page:
        return {'id': page.id, 'title': page.title, 'url': request.route_url('page_get', page_id=page.id)}
    else:
        return {}


@view_config(route_name='backend_json_news_category_list', renderer='json', permission='view')
def backend_json_news_category_list_view(request):
    """回傳最新消息分類的列表"""
    news_category_list = []
    for each_news_category in DAL.get_news_category_list():
        news_category_list.append({'id': each_news_category.id, 'name': each_news_category.name})
    return news_category_list


@view_config(route_name='backend_json_link_category_list', renderer='json', permission='view')
def backend_json_link_category_list_view(request):
    """回傳好站連結分類的列表"""
    link_category_list = []
    for each_link_category in DAL.get_link_category_list():
        link_category_list.append({'id': each_link_category.id, 'name': each_link_category.name})
    return link_category_list
