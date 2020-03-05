from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound

from tp_yass.dal import DAL
from tp_yass.helper import sanitize_input
from tp_yass.forms.backend.user import UserGroupForm


def _recursive_append(group_node, group):
    if group.ancestor_id == group_node['id']:
        group_node['descendants'].append({'id': group.id, 'name': group.name, 'descendants': []})
        return True
    else:
        for descendant_group in group_node['descendants']:
            _recursive_append(descendant_group, group)


def _generate_group_trees():
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
    return group_trees


@view_config(route_name='backend_user_group_list',
             renderer='themes/default/backend/user_group_list.jinja2',
             permission='view')
def backend_user_group_list_view(request):
    return {'group_trees': _generate_group_trees()}


@view_defaults(route_name='backend_user_group_create',
               renderer='themes/default/backend/user_group_create.jinja2',
               permission='edit')
class UserGroupCreateView:
    """建立使用者群組的 view"""

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get_view(self):
        form = UserGroupForm()
        return {'form': form,
                'group_trees': _generate_group_trees()}

    @view_config(request_method='POST')
    def post_view(self):
        form = UserGroupForm(self.request.POST)
        group = DAL.create_group()
        form.populate_obj(group)
        DAL.save_group(group)
        return HTTPFound(location=self.request.route_url('backend_user_group_list'))


@view_config(route_name='backend_user_list',
             renderer='themes/default/backend/user_list.jinja2',
             permission='view')
def backend_user_list_view(request):
    # 每頁顯示的筆數
    quantity_per_page = sanitize_input(request.GET.get('q', 20), int, 20)
    group_id = sanitize_input(request.GET.get('g'), int, None)
    page_id = sanitize_input(request.GET.get('p', 1), int, 1)
    user_list = DAL.get_user_list(page=page_id, group_id=group_id, quantity_per_page=quantity_per_page)
    return {'user_list': user_list,
            'page_quantity_of_total_users': DAL.get_page_quantity_of_total_users(quantity_per_page, group_id),
            'page_id': page_id,
            'quantity_per_page': quantity_per_page}

