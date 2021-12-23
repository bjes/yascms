from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound

from tp_yass.dal import DAL
from tp_yass.forms.backend.account import GroupCreateForm
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
        form = GroupCreateForm()
        return {'form': form,
                'group_trees': generate_group_trees()}

    @view_config(request_method='POST')
    def post_view(self):
        form = GroupCreateForm(self.request.POST)
        form.primary_email.choices = [each_email['address'] for each_email in form.email.data]
        if form.validate():
            group = DAL.create_group()
            self._sync(form, group)
            DAL.save_group(group)
            return HTTPFound(location=self.request.route_url('backend_group_list'))
        return {'form': form,
                'group_trees': generate_group_trees()}

    def _sync(self, form, group):
        """將表單的資料同步給 group model

        Args:
            form: wtforms.Form 物件
            group: tp_yass.models.account.GroupModel

        Returns:
            同步成功回傳 True
        """
        group.name = form.name.data
        email_list = [each_email['address'] for each_email in form.email.data]
        DAL.sync_group_email(group, email_list, form.primary_email.data)
        group.type = form.type.data
        group.order = form.order.data
        group.ancestor_id = form.ancestor_id.data
        return True


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
            primary_email = DAL.get_group_primary_email(group_id)
            form = GroupCreateForm(obj=group)
            if primary_email:
                form.primary_email.data = primary_email
            return {'form': form,
                    'group_trees': generate_group_trees()}
        return HTTPFound(location=self.request.route_url('backend_group_list'))

    @view_config(request_method='POST')
    def post_view(self):
        form = GroupCreateForm(self.request.POST)
        form.primary_email.choices = [each_email['address'] for each_email in form.email.data]
        if form.validate():
            group_id = int(self.request.matchdict['group_id'])
            if group_id <= 2:
                # 內建根群組與管理者群組不能編輯
                self.request.session.flash('內建根群組/內建管理者群組不能編輯', 'fail')
            group = DAL.get_group(group_id)
            if group:
                self._sync(form, group)
                DAL.save_group(group)
        else:
            return {'form': form,
                    'group_trees': generate_group_trees()}
        return HTTPFound(location=self.request.route_url('backend_group_list'))

    def _sync(self, form, group):
        """將表單的資料同步給 group model

        Args:
            form: wtforms.Form 物件
            group: tp_yass.models.account.GroupModel

        Returns:
            同步成功回傳 True
        """
        group.name = form.name.data
        email_list = [each_email['address'] for each_email in form.email.data]
        DAL.sync_group_email(group, email_list, form.primary_email.data)
        group.type = form.type.data
        group.order = form.order.data
        group.ancestor_id = form.ancestor_id.data
        return True


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
