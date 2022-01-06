import logging

from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.view import view_defaults, view_config

from tp_yass.dal import DAL
from tp_yass.enum import GroupType, AuthLogType
from tp_yass.forms.auth import LoginForm


logger = logging.getLogger(__name__)


def create_credential(request, user, auth_source='local'):
    """建立使用者的權限相關設定，比如 session 等資訊

    Args:
        request: pyramid.request.Request
        user: tp_yass.models.account.UserModel
        auth_source: auth 的來源，預設是 local 代表本地認証，若是透過 oauth2 則是傳入 provider 名稱，比如 google

    Returns:
        重導至 backend_homepage
    """
    request.session['user_id'] = user.id
    request.session['first_name'] = user.first_name
    request.session['last_name'] = user.last_name
    request.session['account'] = user.account
    request.session['auth_source'] = auth_source
    request.session['is_admin'] = False
    # 一個帳號可以隸屬多個群組，這邊紀錄隸屬群組的 id 列表
    request.session['main_group_id_list'] = {each_group.id for each_group in user.groups}
    groups = []
    for each_group in user.groups:
        group_tree = []
        current_group = each_group
        while True:
            # 只要有任一個群組（含上層）為管理者權限，則 is_admin 就為 True
            if not request.session['is_admin']:
                if current_group.type == GroupType.ADMIN:
                    request.session['is_admin'] = True
            if current_group.ancestor:
                # 代表還有上層群組
                group_tree.append({'name': current_group.name, 'id': current_group.id, 'type': current_group.type})
                current_group = current_group.ancestor
            else:
                # 代表已經到了最上層群組
                group_tree.append({'name': current_group.name, 'id': current_group.id, 'type': current_group.type})
                groups.append(group_tree)
                break
    # 隸屬群組以及其上的樹狀的群組資料
    request.session['groups'] = groups
    # 紀錄所屬群組以及其以上各樹狀的所有 group id，方便前端網頁處理，才不用埋太多邏輯
    request.session['group_id_list'] = {i['id'] for each_group_list in groups for i in each_group_list}
    DAL.log_auth(AuthLogType.LOGIN, user.id, request.client_addr, auth_source)
    headers = remember(request, user.id)
    return HTTPFound(location=request.route_url('backend_homepage'),
                     headers=headers)


@view_defaults(route_name='login', renderer='')
class LoginView:
    """登入"""

    def __init__(self, request):
        self.request = request
        self.request.override_renderer = f'themes/{self.request.effective_theme_name}/frontend/login.jinja2'

    @view_config(request_method='GET')
    def get(self):
        if self.request.session.get('account'):
            return HTTPFound(location=self.request.route_url('backend_homepage'))
        else:
            oauth2_provider_info_list = []
            oauth2_integration_config = DAL.get_oauth2_integration_config()
            for each_provider in oauth2_integration_config:
                if oauth2_integration_config[each_provider]['settings']['enabled']:
                    oauth2_provider_info_list.append({'name': each_provider,
                                                          'canonical_name': oauth2_integration_config[each_provider]['canonical_name']})
            return {'login_form': LoginForm(), 'oauth2_provider_info_list': oauth2_provider_info_list}

    @view_config(request_method='POST')
    def post(self):
        login_form = LoginForm(self.request.POST)
        if login_form.validate():
            user = DAL.auth_user(login_form.account.data,
                                 login_form.password.data)
            if user:
                return create_credential(self.request, user)
            else:
                user = DAL.get_user_account(login_form.account.data)
                if user:
                    DAL.log_auth(AuthLogType.WRONG_PASSWORD, user.id, self.request.client_addr)
                else:
                    logger.warning('帳號 "%s" 不存在', login_form.account.data)
                self.request.session.flash('登入失敗，請檢查帳號密碼是否有誤', 'fail')
        else:
            logger.error('表單驗證失敗，可能有人入侵：account 欄位為 "%s"，password 欄位為 "%s"',
                         login_form.account.data, login_form.password.data)
        return {'login_form': login_form}
