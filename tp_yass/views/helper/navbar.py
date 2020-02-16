from tp_yass.dal import DAL


def _recursive_append(navbar_node, navbar):
    """遞迴的產生 sub navbar"""

    # 代表這是不可變動的選單，其 id 才會是 -1
    if navbar_node['id'] == -1:
        return True
    # leaf node
    elif navbar.ancestor_id == navbar_node['id']:
        sub_navbar = {'id': navbar.id,
                      'name': navbar.name,
                      'url': navbar.url,
                      'is_external': navbar.is_external,
                      'icon': navbar.icon,
                      'type': navbar.type,
                      'module_name': navbar.module_name,
                      'order': navbar.order,
                      'descendants': []}
        if navbar.type == 4 and navbar.module_name == 'news':
            sub_navbar['descendants'] = news_factory()
        navbar_node['descendants'].append(sub_navbar)
        return True
    # 繼續往下一層對應
    else:
        for descendant_navbar in navbar_node['descendants']:
            _recursive_append(descendant_navbar, navbar)


def generate_navbar_trees(navbar_list):
    """將傳入的 navbar list orms 轉成單純的 巢狀陣列，避免相依後端的 orm"""
    navbar_trees = []
    for navbar in navbar_list:
        if not navbar.ancestor_id:
            # 代表是最上層導覽列
            sub_navbar = {'id': navbar.id,
                          'name': navbar.name,
                          'url': navbar.url,
                          'is_external': navbar.is_external,
                          'icon': navbar.icon,
                          'type': navbar.type,
                          'module_name': navbar.module_name,
                          'order': navbar.order,
                          'descendants': []}
            if navbar.type == 4 and navbar.module_name == 'news':
                sub_navbar['descendants'] = news_factory()
            navbar_trees.append(sub_navbar)
        else:
            # 代表是第二層以下的群組
            for root_node in navbar_trees:
                if _recursive_append(root_node, navbar):
                    break
    return navbar_trees

def news_factory():
    sub_navbars = []
    for each_category in DAL.get_news_category_list():
        # 遞迴處理 navbar 時都會用 id 判斷階層關係，這邊設定為 -1 保證不會對到
        # (None) 意思代表為 root_node 所以不適合採用，故改用 -1
        sub_navbars.append({'id': -1,
                            'type': 'news_category',
                            'category_id': each_category.id,
                            'category_name': each_category.name,
                            'category_url': '#'})
    sub_navbars.append({'id': -1,
                        'type': 'news_divider'})
    sub_navbars.append({'id': -1,
                        'type': 'news_show_all'})
    return sub_navbars
