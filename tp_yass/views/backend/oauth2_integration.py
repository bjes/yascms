import json
import logging

from pyramid.view import view_config, view_defaults

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
