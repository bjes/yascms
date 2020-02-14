def _recursive_append(navbar_node, navbar):
    if navbar.ancestor_id == navbar_node['id']:
        navbar_node['descendants'].append({'id': navbar.id,
                                           'name': navbar.name,
                                           'url': navbar.url,
                                           'is_external': navbar.is_external,
                                           'icon': navbar.icon,
                                           'type': navbar.type,
                                           'module_name': navbar.module_name,
                                           'order': navbar.order,
                                           'descendants': []})
        return True
    else:
        for descendant_navbar in navbar_node['descendants']:
            _recursive_append(descendant_navbar, navbar)


def generate_navbar_trees(navbar_list):
    navbar_trees = []
    for navbar in navbar_list:
        if not navbar.ancestor_id:
            # 代表是最上層導覽列
            navbar_trees.append({'id': navbar.id,
                                 'name': navbar.name,
                                 'url': navbar.url,
                                 'is_external': navbar.is_external,
                                 'icon': navbar.icon,
                                 'type': navbar.type,
                                 'module_name': navbar.module_name,
                                 'order': navbar.order,
                                 'descendants': []})
        else:
            # 代表是第二層以下的群組
            for root_node in navbar_trees:
                if _recursive_append(root_node, navbar):
                    break
    return navbar_trees
