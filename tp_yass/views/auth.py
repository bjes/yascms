import logging

from pyramid.view import view_config, view_defaults
from pyramid.security import remember, forget
from pyramid.httpexceptions import HTTPFound

from tp_yass.forms.auth import LoginForm
from tp_yass.dal import DAL


logger = logging.getLogger(__name__)


@view_defaults(route_name='login', renderer='themes/default/login.jinja2')
class LoginView:

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get(self):
        if self.request.session.get('account'):
            return HTTPFound(location=self.request.route_url('backend_homepage'))
        else:
            return {'login_form': LoginForm()}

    @view_config(request_method='POST')
    def post(self):
        login_form = LoginForm(self.request.POST)
        if login_form.validate():
            user = DAL.auth_user(login_form.account.data,
                                 login_form.password.data)
            if user:
                self.request.session['user_id'] = user.id
                self.request.session['first_name'] = user.first_name
                self.request.session['last_name'] = user.last_name
                self.request.session['account'] = user.account
                self.request.session['is_admin'] = False
                self.request.session['main_group_id_list'] = [each_group.id for each_group in user.groups]
                groups = []
                for each_group in user.groups:
                    group_tree = []
                    current_group = each_group
                    while True:
                        # 只要有任一個群組（含上層）為管理者權限，則 is_admin 就為 True
                        if not self.request.session['is_admin']:
                            if current_group.type == 0:
                                self.request.session['is_admin'] = True
                        if current_group.ancestor:
                            # 代表還有上層群組
                            group_tree.append({'name': current_group.name, 'id': current_group.id,'type': current_group.type})
                            current_group = current_group.ancestor
                        else:
                            # 代表已經到了最上層群組
                            group_tree.append({'name': current_group.name, 'id': current_group.id,'type': current_group.type})
                            groups.append(group_tree)
                            break
                self.request.session['groups'] = groups
                self.request.session['group_id_list'] = list({i['id'] for each_group_list in groups for i in each_group_list})
                logger.info('帳號 "%s" 已登入', user.account)
                logger.debug('帳號 "%s" 存在 session 的 groups 為 %s', user.account, groups)
                logger.debug('帳號 "%s" 存在 session 的 group_id_list 為 %s', user.account, self.request.session['group_id_list'])
                if self.request.session['is_admin']:
                    logger.debug('帳號 "%s" 有管理者權限', user.account)
                headers = remember(self.request, user.account)
                return HTTPFound(location=self.request.route_url('backend_homepage'),
                                 headers=headers)
            else:
                logger.warning('帳號 "%s" 登入失敗', login_form.account.data)
                self.request.session.flash('登入失敗，請檢查帳號密碼是否有誤', 'fail')
        else:
            logger.error('表單驗證失敗，可能有人入侵：account 欄位為 "%s"，password 欄位為 "%s"',
                         login_form.account.data, login_form.password.data)
        return {'login_form': login_form}


class LogoutView:

    def __init__(self, request):
        self.request = request

    @view_config(route_name='logout')
    def logout(self):
        headers = forget(self.request)
        account = self.request.session['account']
        self.request.session.clear()
        logger.info('帳號 "%s" 已登出', account)
        return HTTPFound(location=self.request.route_url('homepage'),
                         headers=headers)

