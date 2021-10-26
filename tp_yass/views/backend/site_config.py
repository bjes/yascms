import logging

from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound

from tp_yass.dal import DAL

logger = logging.getLogger(__name__)


@view_defaults(route_name='backend_site_config_edit',
               renderer='',
               permission='edit')
class SiteConfigView:

    def __init__(self, request):
        self.request = request
        self.request.override_renderer = f'themes/{request.effective_theme_name}/backend/site_config_edit.jinja2'

    @view_config(request_method='GET')
    def list_view(self):
        """列出 site config 列表"""

        config_list = DAL.get_site_config_list()
        return {'config_list': config_list}

    def _validate(self, post_data):
        """跟資料庫的 sys config 比對，除了驗證資料類型之外，只回傳需要更改的 config list

        Args:
            post_data: pyramid 的 request.POST
        Returns:
            回傳需要更新的 list
        """
        db_site_config_list = DAL.get_site_config_list()
        updated_config_list = []
        for key, value in post_data.items():
            for each_config in db_site_config_list:
                if key == each_config.name:
                    if not value:
                        logger.error('系統設定 %s 其值為空', key)
                        return False
                    if each_config.type == 'int' and not value.isdigit():
                        logger.error('系統設定 %s 其值 %s 不合法 int', key, value)
                        return False
                    if each_config.type == 'bool' and value not in ('true', 'false'):
                        logger.error('系統設定 %s 其值 %s 不是合法 bool', key, value)
                        return False
                    if value != each_config.value:
                        updated_config_list.append({'id': each_config.id, 'name': key, 'value': value})
                        break
        return updated_config_list

    @view_config(request_method='POST')
    def post_view(self):
        """更新系統設定"""

        updated_config_list = self._validate(self.request.POST)
        if updated_config_list:
            DAL.update_site_config_list(updated_config_list)
            self.request.session.flash('更新設定成功', 'success')
            self.request.cache.delete_site_config()
            return HTTPFound(location=self.request.current_route_url())
        else:
            self.request.session.flash('設定沒有異動', 'fail')
            return HTTPFound(location=self.request.current_route_url())
