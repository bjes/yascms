import json

from pyramid.view import view_config, view_defaults

from tp_yass.dal import DAL


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
        oauth2_integration_settings = json.loads(DAL.get_oauth2_integration_settings())
        for each_provider in oauth2_integration_settings:
            provider_list.append({'name': each_provider,
                                  'enabled': oauth2_integration_settings[each_provider]['settings']['enabled']})
        return {'provider_list': provider_list}
