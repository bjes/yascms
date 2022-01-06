import json
import logging

from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from tp_yass.dal import DAL


logger = logging.getLogger(__name__)


@view_defaults(route_name='backend_oauth2_integration_list', renderer='', permission='view')
class OAuth2IntegrationListView:

    def __init__(self, request):
        """
        Args:
            request: pyramid.request.Request
        """
        self.request = request
        self.request.override_renderer = f'themes/{self.request.effective_theme_name}/backend/oauth2_integration_list.jinja2'

    @view_config(request_method='GET')
    def get_view(self):
        """顯示目前支援的 OAuth2 Providers 列表"""
        provider_list = []
        oauth2_integration_config = json.loads(DAL.get_oauth2_integration_config())
        for each_provider in oauth2_integration_config:
            provider_list.append({'name': oauth2_integration_config[each_provider]['canonical_name'],
                                  'enabled': oauth2_integration_config[each_provider]['settings']['enabled']})
        return {'provider_list': provider_list}


@view_defaults(route_name='backend_oauth2_integration_edit', renderer='', permission='edit')
class OAuth2IntegrationEditView:

    def __init__(self, request):
        """
        Args:
            request: pyramid.request.Request
        """
        self.request = request
        self.request.override_renderer = f'themes/{self.request.effective_theme_name}/backend/oauth2_integration_edit.jinja2'

    @view_config(request_method='GET')
    def get_view(self):
        """顯示指定 provider 的設定"""
        provider_name = self.request.matchdict['provider_name']
        oauth_integration_config = DAL.get_oauth2_integration_config()
        if provider_name in oauth_integration_config:
           return {'provider_config': oauth_integration_config[provider_name]}
        else:
            logger.error('找不到 Provider %s', provider_name)
            return HTTPNotFound()
