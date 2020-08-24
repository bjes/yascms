from tp_yass.enum import NavbarType
from tp_yass.dal import DAL


def _recursive_append(request, navbar_node, navbar):
    """遞迴的產生 sub navbar"""

    # 代表這是不可變動的選單，其 id 才會是 -1
    if navbar_node['id'] == -1:
        return True
    # leaf node
    elif navbar.ancestor_id == navbar_node['id']:
        if navbar.page:
            url = request.route_path('page_get', page_id=navbar.page.id)
        else:
            url = navbar.url
        sub_navbar = {'id': navbar.id,
                      'name': navbar.name,
                      'aria_name': navbar.aria_name,
                      'url': url,
                      'is_external': navbar.is_external,
                      'icon': navbar.icon,
                      'type': NavbarType(navbar.type),
                      'module_name': navbar.module_name,
                      'order': navbar.order,
                      'descendants': []}
        if navbar.type == NavbarType.BUILTIN_NEWS:
            sub_navbar['descendants'] = news_factory()
        elif navbar.type == NavbarType.BUILTIN_CALENDAR:
            sub_navbar['url'] = request.route_path('calendar')
        navbar_node['descendants'].append(sub_navbar)
        return True
    # 繼續往下一層對應
    else:
        for descendant_navbar in navbar_node['descendants']:
            _recursive_append(request, descendant_navbar, navbar)


def generate_navbar_trees(request, type='all', visible_only=False, excluded_id=None):
    """將傳 navbar list orm 轉成單純的巢狀陣列，避免相依後端的 orm

    Args:
        request: pyramid.request.Request
        type: 傳入 DAL.get_navbar_list 用
        visible_only: 傳入 DAL.get_navbar_list 用

    Returns:
        回傳 navbar 樹狀結構
    """
    navbar_trees = []
    for navbar in DAL.get_navbar_list(type, visible_only, excluded_id):
        if not navbar.ancestor_id:
            # 代表是最上層導覽列
            if navbar.page:
                url = request.route_path('page_get', page_id=navbar.page.id)
            else:
                url = navbar.url
            sub_navbar = {'id': navbar.id,
                          'name': navbar.name,
                          'aria_name': navbar.aria_name,
                          'url': url,
                          'is_external': navbar.is_external,
                          'icon': navbar.icon,
                          'type': NavbarType(navbar.type),
                          'module_name': navbar.module_name,
                          'order': navbar.order,
                          'descendants': []}
            if navbar.type == NavbarType.BUILTIN_NEWS:
                sub_navbar['descendants'] = news_factory()
            navbar_trees.append(sub_navbar)
        else:
            # 代表是第二層以下的群組
            for root_node in navbar_trees:
                if _recursive_append(request, root_node, navbar):
                    break
    return navbar_trees

def news_factory():
    """存在資料庫的 navbar 只有 news 一筆 record，在這邊要手動的把子選單加進去"""
    sub_navbars = []
    for each_category in DAL.get_news_category_list():
        # 遞迴處理 navbar 時都會用 id 判斷階層關係，這邊設定為 -1 代表是 builtin
        sub_navbars.append({'id': -1,
                            'type': NavbarType.BUILTIN_NEWS_SUBTYPE,
                            'category_id': each_category.id,  # 這個欄位是額外加上去的，因為要產生連結的 url 需要 category id
                            'name': each_category.name,
                            'url': '#'})
    # 分隔線，這個是寫死在 news 子選單裡面，沒有要給使用者異動位置，所以 id 也是 -1
    sub_navbars.append({'id': -1,
                        'type': NavbarType.DROPDOWN_DIVIDER,
                        'name': '分隔線'})
    # 顯示全部最新消息的連結
    sub_navbars.append({'id': -1,
                        'type': NavbarType.BUILTIN_NEWS_ALL})
    return sub_navbars
