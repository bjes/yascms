import logging

from pyramid.view import view_defaults, view_config
from pyramid.httpexceptions import HTTPFound

from tp_yass.dal import DAL
from tp_yass.forms.backend.api_token import APITokenForm
from tp_yass.enum import EnabledType


logger = logging.getLogger(__name__)


@view_defaults(route_name='backend_api_token_list', renderer='', permission='view')
class APITokenListView:
    """列表 api token 的 view"""

    def __init__(self, request):
        self.request = request
        self.request.override_renderer = f'themes/{self.request.effective_theme_name}/backend/api_token_list.jinja2'

    @view_config()
    def get_view(self):
        return {'api_token_list': DAL.get_api_token_list()}


@view_defaults(route_name='backend_api_token_create', renderer='', permission='edit')
class APITokenCreateView:
    """新增 api token 的 view"""

    def __init__(self, request):
        self.request = request
        self.request.override_renderer = f'themes/{self.request.effective_theme_name}/backend/api_token_create.jinja2'

    @view_config(request_method='GET')
    def get_view(self):
        return {'form': APITokenForm()}

    @view_config(request_method='POST')
    def post_view(self):
        form = APITokenForm(self.request.POST)
        if form.validate():
            api_token = DAL.create_api_token()
            api_token.name = form.name.data
            if form.description.data and form.description.data.strip():
                api_token.description = form.description.data
            if form.is_enabled.data:
                api_token.is_enabled = EnabledType.IS_ENABLED.value
            else:
                api_token.is_enabled = EnabledType.IS_NOT_ENABLED.value
            DAL.save_api_token(api_token)
            self.request.session.flash('建立 API 金鑰成功', 'success')
            return HTTPFound(location=self.request.route_url('backend_api_token_list'))
        return {'form': APITokenForm()}
