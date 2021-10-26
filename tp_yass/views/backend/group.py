from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound

from tp_yass.dal import DAL
from tp_yass.forms.backend.user import GroupForm
from tp_yass.helpers.backend.group import generate_group_trees
from tp_yass.enum import GroupType


@view_defaults(route_name='backend_group_list',
               renderer='',
               permission='view')
class GroupListView:
    """列表使用者群組的 view"""

    def __init__(self, request):
        self.request = request
        self.request.override_renderer = f'themes/{self.request.effective_theme_name}/backend/group_list.jinja2'

    @view_config()
    def get_view(self):
        return {'group_trees': generate_group_trees(), 'GroupType': GroupType}


@view_defaults(route_name='backend_group_create',
               renderer='',
               permission='edit')
class GroupCreateView:
    """建立使用者群組的 view"""

    def __init__(self, request):
        self.request = request
        self.request.override_renderer = f'themes/{self.request.effective_theme_name}/backend/group_create.jinja2'

    @view_config(request_method='GET')
    def get_view(self):
        form = GroupForm()
        return {'form': form,
                'group_trees': generate_group_trees()}

    @view_config(request_method='POST')
    def post_view(self):
        form = GroupForm(self.request.POST)
        if form.validate():
            group = DAL.create_group()
            form.populate_obj(group)
            DAL.save_group(group)
            return HTTPFound(location=self.request.route_url('backend_group_list'))
        return {'form': form,
                'group_trees': generate_group_trees()}


@view_defaults(route_name='backend_group_edit',
               renderer='',
               permission='edit')
class GroupEditView:
    """編輯使用者群組的 view"""

    def __init__(self, request):
        self.request = request
        self.request.override_renderer = f'themes/{self.request.effective_theme_name}/backend/group_edit.jinja2'

    @view_config(request_method='GET')
    def get_view(self):
        group_id = int(self.request.matchdict['group_id'])
        if group_id <= 2:
            # 內建根群組與管理者群組不能編輯
            self.request.session.flash('內建根群組/內建管理者群組不能編輯', 'fail')
            return HTTPFound(location=self.request.route_url('backend_group_list'))
        group = DAL.get_group(group_id)
        if group:
            form = GroupForm(obj=group)
            return {'form': form,
                    'group_trees': generate_group_trees()}
        return HTTPFound(location=self.request.route_url('backend_group_list'))

    @view_config(request_method='POST')
    def post_view(self):
        form = GroupForm(self.request.POST)
        if form.validate():
            group_id = int(self.request.matchdict['group_id'])
            if group_id <= 2:
                # 內建根群組與管理者群組不能編輯
                self.request.session.flash('內建根群組/內建管理者群組不能編輯', 'fail')
                return HTTPFound(location=self.request.route_url('backend_group_list'))
            group = DAL.get_group(group_id)
            if group:
                form.populate_obj(group)
                DAL.save_group(group)
            return HTTPFound(location=self.request.route_url('backend_group_list'))
        return {'form': form,
                'group_trees': generate_group_trees()}


@view_defaults(route_name='backend_group_delete', permission='edit')
class GroupDeleteView:
    """刪除使用者群組的 view"""

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get_view(self):
        group_id = int(self.request.matchdict['group_id'])
        if group_id <= 2:
            # 內建的根群組與最高管理者群組不能砍
            self.request.session.flash('管理者群組不能刪除', 'fail')
            return HTTPFound(location=self.request.route_url('backend_group_list'))
        group = DAL.get_group(group_id)
        if group:
            DAL.change_group_ancestor_id(group_id, group.ancestor_id)
            DAL.delete_group(group)
        else:
            self.request.session.flash('找不到指定群組', 'fail')
        return HTTPFound(location=self.request.route_url('backend_group_list'))
