from pyramid.view import view_config

from tp_yass.dal import DAL


def _recursive_append(group_node, group):
    if group.ancestor_id == group_node['id']:
        group_node['descendants'].append({'id': group.id, 'name': group.name, 'descendants': []})
        return True
    else:
        for descendant_group in group_node['descendants']:
            _recursive_append(descendant_group, group)

@view_config(route_name='backend_user_group_list',
             renderer='themes/default/backend/user_group_list.jinja2',
             permission='view')
def backend_user_group_list_view(request):
    all_groups = DAL.get_user_group_list()
    group_trees = []
    for group in all_groups:
        if not group.ancestor_id:
            # 代表是最上層群組
            group_trees.append({'id': group.id, 'name': group.name, 'descendants': []})
        else:
            # 代表是第二層以下的群組
            for root_node in group_trees:
                if _recursive_append(root_node, group):
                    break
    return {'group_trees': group_trees}
