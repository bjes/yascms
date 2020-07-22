from pyramid.view import view_config
from tp_yass.dal import DAL


@view_config(route_name='backend_api_page_list', renderer='json', permission='view')
def backend_api_page_list(request):
    """回傳單一頁面的列表 json"""
    page_list = []
    for each_page in DAL.get_page_list(pagination=False):
        page_list.append({'id': each_page.id,
                          'title': each_page.title,
                          'url': request.route_url('page_get', page_id=each_page.id)})
    return page_list


@view_config(route_name='backend_api_page_get', renderer='json', permission='view')
def backend_api_page_get(request):
    """回傳單一頁面的 json"""
    page = DAL.get_page(int(request.matchdict['page_id']))
    if page:
        return {'id': page.id, 'title': page.title, 'url': request.route_url('page_get', page_id=page.id)}
    else:
        return {}
