from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound

from tp_yass.dal import DAL
from tp_yass.helpers import sanitize_input
from tp_yass.forms.backend.account import UserCreateForm, UserEditForm
from tp_yass.helpers.backend.group import generate_group_trees
from tp_yass.enum import EmailType


@view_defaults(route_name='backend_user_list',
               renderer='',
               permission='view')
class UserListView:
    """列表使用者的 view"""

    def __init__(self, request):
        self.request = request
        self.request.override_renderer = f'themes/{self.request.effective_theme_name}/backend/user_list.jinja2'

    @view_config()
    def get_view(self):
        # 每頁顯示的筆數
        quantity_per_page = sanitize_input(self.request.GET.get('q', 20), int, 20)
        group_id = sanitize_input(self.request.GET.get('g'), int, None)
        page_id = sanitize_input(self.request.GET.get('p', 1), int, 1)
        user_list = DAL.get_user_list(page=page_id, group_id=group_id, quantity_per_page=quantity_per_page)
        return {'user_list': user_list,
                'EmailType': EmailType,
                'page_quantity_of_total_users': DAL.get_page_quantity_of_total_users(quantity_per_page, group_id),
                'page_id': page_id,
                'quantity_per_page': quantity_per_page}


@view_defaults(route_name='backend_user_create',
               renderer='',
               permission='edit')
class UserCreateView:
    """新增使用者的 view"""

    def __init__(self, request):
        self.request = request
        self.request.override_renderer = f'themes/{self.request.effective_theme_name}/backend/user_create.jinja2'

    @view_config(request_method='GET')
    def get_view(self):
        form = UserCreateForm()
        return {'form': form,
                'group_trees': generate_group_trees()}

    @view_config(request_method='POST')
    def post_view(self):
        form = UserCreateForm()
        form.group_ids.choices = [(each_group.id, each_group.name) for each_group in DAL.get_group_list()]
        form.process(self.request.POST)
        form.primary_email.choices = [each_email_form.form.address.data for each_email_form in form.email]
        if form.validate():
            user = DAL.create_user()
            existed_account = DAL.get_user_account(form.account.data)
            if existed_account:
                self.request.session.flash('帳號名稱已存在，請改用其他名稱', 'fail')
                return {'form': form,
                        'group_ids': form.group_ids.data,
                        'group_trees': generate_group_trees()}
            self._sync(form, user)
            DAL.save_user(user)
            return HTTPFound(location=self.request.route_url('backend_user_list'))
        return {'form': form,
                'group_ids': form.group_ids.data,
                'group_trees': generate_group_trees()}

    def _sync(self, form, user):
        """將表單的資料同步給 user model

        Args:
            form: wtforms.Form 物件
            user: tp_yass.models.account

        Returns:
            同步成功回傳 True
        """
        user.password = form.password.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        email_list = [each_email['address'] for each_email in form.email.data]
        DAL.sync_user_email(user, email_list, form.primary_email.data)
        user.account = form.account.data
        user.groups = DAL.get_groups(form.group_ids.data)
        return True

@view_defaults(route_name='backend_user_edit',
               renderer='',
               permission='edit')
class UserEditView:
    """編輯使用者的 view"""

    def __init__(self, request):
        self.request = request
        self.request.override_renderer = f'themes/{self.request.effective_theme_name}/backend/user_edit.jinja2'

    @view_config(request_method='GET')
    def get_view(self):
        user_id = int(self.request.matchdict['user_id'])
        user = DAL.get_user(user_id)
        if user:
            primary_email = DAL.get_user_primary_email(user)
            form = UserEditForm(obj=user)
            form.primary_email.data = primary_email
            group_ids = [each_group.id for each_group in user.groups]
            return {'form': form,
                    'group_ids': group_ids,
                    'group_trees': generate_group_trees()}
        return HTTPFound(location=self.request.route_url('backend_user_list'))

    @view_config(request_method='POST')
    def post_view(self):
        form = UserEditForm()
        form.group_ids.choices = [(each_group.id, each_group.name) for each_group in DAL.get_group_list()]
        form.process(self.request.POST)
        form.primary_email.choices = [each_email_form.form.address.data for each_email_form in form.email]
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
                self._sync(form, user)
                DAL.save_user(user)
        else:
            return {'form': form,
                    'group_ids': form.group_ids.data,
                    'group_trees': generate_group_trees()}
        return HTTPFound(location=self.request.route_url('backend_user_list'))

    def _sync(self, form, user):
        """將表單的資料同步給 user model

        Args:
            form: wtforms.Form 物件
            user: tp_yass.models.account

        Returns:
            同步成功回傳 True
        """
        # 如果密碼欄位不為空，視做要改密碼，否則密碼不變動
        if form.password.data:
            user.password = form.password.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        email_list = [each_email['address'] for each_email in form.email.data]
        DAL.sync_user_email(user, email_list, form.primary_email.data)
        user.account = form.account.data
        # 系統預設建立的管理者帳號其群組不能變動
        if user.id != 1:
            user.groups = DAL.get_groups(form.group_ids.data)
        return True

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
