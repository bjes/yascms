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
        for each_provider in json.loads(DAL.get_oauth2_integration_list()):
            provider_list.append(each_provider)
        return {'provider_list': provider_list}
