from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound

from tp_yass.dal import DAL
from tp_yass.helper import sanitize_input
from tp_yass.forms.backend.user import UserGroupForm, UserForm, UserEditForm
from tp_yass.views.backend.helper import generate_group_trees


@view_defaults(route_name='backend_user_group_list',
               renderer='themes/default/backend/user_group_list.jinja2',
               permission='view')
class UserGroupListView:
    """列表使用者群組的 view"""

    def __init__(self, request):
        self.request = request

    @view_config()
    def get_view(self):
        return {'group_trees': generate_group_trees()}


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
                'group_trees': generate_group_trees()}

    @view_config(request_method='POST')
    def post_view(self):
        form = UserGroupForm(self.request.POST)
        if form.validate():
            group = DAL.create_group()
            form.populate_obj(group)
            DAL.save_group(group)
            return HTTPFound(location=self.request.route_url('backend_user_group_list'))
        return {'form': form,
                'group_trees': generate_group_trees()}


@view_defaults(route_name='backend_user_group_edit',
               renderer='themes/default/backend/user_group_edit.jinja2',
               permission='edit')
class UserGroupEditView:
    """編輯使用者群組的 view"""

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get_view(self):
        group_id = int(self.request.matchdict['group_id'])
        if group_id == 1:
            # 管理者群組不能編輯
            self.request.session.flash('管理者群組不能編輯', 'fail')
            return HTTPFound(location=self.request.route_url('backend_user_group_list'))
        group = DAL.get_group(group_id)
        if group:
            form = UserGroupForm(obj=group)
            return {'form': form,
                    'group_trees': generate_group_trees()}
        return HTTPFound(location=self.request.route_url('backend_user_group_list'))

    @view_config(request_method='POST')
    def post_view(self):
        form = UserGroupForm(self.request.POST)
        if form.validate():
            group_id = int(self.request.matchdict['group_id'])
            if group_id == 1:
                # 管理者群組不能編輯
                self.request.session.flash('管理者群組不能編輯', 'fail')
                return HTTPFound(location=self.request.route_url('backend_user_group_list'))
            group = DAL.get_group(group_id)
            if group:
                form.populate_obj(group)
                DAL.save_group(group)
            return HTTPFound(location=self.request.route_url('backend_user_group_list'))
        return {'form': form,
                'group_trees': generate_group_trees()}


@view_defaults(route_name='backend_user_group_delete', permission='edit')
class UserGroupDeleteView:
    """刪除使用者群組的 view"""

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get_view(self):
        group_id = int(self.request.matchdict['group_id'])
        if group_id == 1:
            # 管理者群組不能砍
            self.request.session.flash('管理者群組不能刪除', 'fail')
            return HTTPFound(location=self.request.route_url('backend_user_group_list'))
        group = DAL.get_group(group_id)
        for each_child in group.descendants:
            each_child.ancestor = group.ancestor
            DAL.save_group(each_child)
        DAL.delete_group(group)
        return HTTPFound(location=self.request.route_url('backend_user_group_list'))


@view_defaults(route_name='backend_user_list',
               renderer='themes/default/backend/user_list.jinja2',
               permission='view')
class UserListView:
    """列表使用者的 view"""

    def __init__(self, request):
        self.request = request

    @view_config()
    def get_view(self):
        # 每頁顯示的筆數
        quantity_per_page = sanitize_input(self.request.GET.get('q', 20), int, 20)
        group_id = sanitize_input(self.request.GET.get('g'), int, None)
        page_id = sanitize_input(self.request.GET.get('p', 1), int, 1)
        user_list = DAL.get_user_list(page=page_id, group_id=group_id, quantity_per_page=quantity_per_page)
        return {'user_list': user_list,
                'page_quantity_of_total_users': DAL.get_page_quantity_of_total_users(quantity_per_page, group_id),
                'page_id': page_id,
                'quantity_per_page': quantity_per_page}


@view_defaults(route_name='backend_user_create',
               renderer='themes/default/backend/user_create.jinja2',
               permission='edit')
class UserCreateView:
    """新增使用者的 view"""

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get_view(self):
        form = UserForm()
        return {'form': form,
                'group_trees': generate_group_trees()}

    @view_config(request_method='POST')
    def post_view(self):
        form = UserForm()
        form.group_ids.choices = [(each_group.id, each_group.name) for each_group in DAL.get_user_group_list()]
        form.process(self.request.POST)
        if form.validate():
            user = DAL.create_user()
            form.populate_obj(user)
            user.groups = DAL.get_groups(form.group_ids.data)
            DAL.save_user(user)
            return HTTPFound(location=self.request.route_url('backend_user_list'))
        return {'form': form,
                'group_trees': generate_group_trees()}


@view_defaults(route_name='backend_user_edit',
               renderer='themes/default/backend/user_edit.jinja2',
               permission='edit')
class UserEditView:
    """編輯使用者的 view"""

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get_view(self):
        user_id = int(self.request.matchdict['user_id'])
        user = DAL.get_user(user_id)
        if user:
            form = UserEditForm(obj=user)
            group_ids = [each_group.id for each_group in user.groups]
            return {'form': form,
                    'group_ids': group_ids,
                    'group_trees': generate_group_trees()}
        return HTTPFound(location=self.request.route_url('backend_user_list'))

    @view_config(request_method='POST')
    def post_view(self):
        form = UserEditForm()
        form.group_ids.choices = [(each_group.id, each_group.name) for each_group in DAL.get_user_group_list()]
        form.process(self.request.POST)
        if form.validate():
            user_id = int(self.request.matchdict['user_id'])
            user = DAL.get_user(user_id)
            if user:
                existed_account = DAL.get_user_account(form.account.data)
                if existed_account and (existed_account.id != user_id):
                    self.request.session.flash('帳號名稱已存在，請改用其他名稱', 'fail')
                    return {'form': form,
                            'group_ids': form.group_ids.data,
                            'group_trees': generate_group_trees()}
                # 如果密碼欄位不為空，視做要改密碼，否則密碼不變動
                if form.password.data:
                    form.populate_obj(user)
                else:
                    ori_password = user._password
                    form.populate_obj(user)
                    user._password = ori_password
                # 管理者的帳號其群組不能變動
                if user_id != 1:
                    user.groups = DAL.get_groups(form.group_ids.data)
                DAL.save_user(user)
        else:
            return {'form': form,
                    'group_ids': form.group_ids.data,
                    'group_trees': generate_group_trees()}
        return HTTPFound(location=self.request.route_url('backend_user_list'))


@view_defaults(route_name='backend_user_delete', permission='edit')
class UserDeleteView:
    """刪除使用者的 view"""

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get_view(self):
        user_id = int(self.request.matchdict['user_id'])
        if user_id == 1:
            # 管理者不能刪除
            self.request.session.flash('管理者不能刪除', 'fail')
            return HTTPFound(location=self.request.route_url('backend_user_list'))
        user = DAL.get_user(user_id)
        if user:
            DAL.delete_user(user)
        return HTTPFound(location=self.request.route_url('backend_user_list'))
