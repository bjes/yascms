from tp_yass.dal import DAL
from tp_yass.enum import GroupType


def _generate_inheritance_data(sub_group_trees, inherited_permission):
    """上層 node 的權限會繼承至下層的 node，權限高低依序是 ADMIN > STAFF > NORMAL

    Args:
        sub_group_trees: 由 generate_group_trees() 產生的 group_trees 移掉最上層的 json 資料結構，移掉一層才好用遞迴處理
        inherited_permission: 目前所繼承的權限
    """
    if sub_group_trees['type'] <= inherited_permission:
        sub_group_trees['inheritance'] = sub_group_trees['type']
    else:
        sub_group_trees['inheritance'] = inherited_permission

    for each_group in sub_group_trees['descendants']:
        if each_group['descendants']:
            _generate_inheritance_data(each_group, sub_group_trees['inheritance'])
        else:
            if each_group['type'] <= sub_group_trees['inheritance']:
                each_group['inheritance'] = each_group['type']
            else:
                each_group['inheritance'] = sub_group_trees['inheritance']


def _recursive_append(group_node, group):
    if group.ancestor_id == group_node['id']:
        descendant = {'id': group.id,
                      'name': group.name,
                      'email': [{'address': each_email.address, 'type': each_email.type} for each_email in group.email],
                      'type': group.type,
                      'inheritance': GroupType.NORMAL.value,  # 預設是普通權限
                      'descendants': []}
        group_node['descendants'].append(descendant)
        return True
    else:
        for descendant_group in group_node['descendants']:
            _recursive_append(descendant_group, group)


def generate_group_trees():
    """產生前端需要的 group trees json 資料結構"""
    all_groups = DAL.get_group_list()
    group_trees = {}
    for group in all_groups:
        if not group.ancestor_id:
            # 代表是最上層群組，最上層群組是根群組，預設的繼承權限為 GroupType.NORMAL
            group_trees = {'id': group.id,
                           'name': group.name,
                           'email': [{'address': each_email.address, 'type': each_email.type} for each_email in group.email],
                           'type': group.type,
                           'inheritance': GroupType.NORMAL.value,
                           'descendants': []}
        else:
            # 代表是第二層以下的群組
            _recursive_append(group_trees, group)
    _generate_inheritance_data(group_trees, GroupType.NORMAL.value)
    return group_trees
