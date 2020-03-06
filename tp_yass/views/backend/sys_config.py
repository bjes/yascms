import logging
from pathlib import Path

from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound

import tp_yass
from tp_yass.dal import DAL
from tp_yass.views.helper.file import get_project_abspath


logger = logging.getLogger(__name__)


@view_defaults(route_name='backend_sys_config_edit',
               renderer='tp_yass:themes/default/backend/sys_config_edit.jinja2',
               permission='edit')
class SysConfigView:

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def list_view(self):
        """列出 tp_yass:themes 目錄下扣掉 default 後有哪些樣板"""

        # TODO: 不要顯示 maintenance mode
        config_list = DAL.get_sys_config_list()
        available_themes_list = self._get_themes_list()
        return {'config_list': config_list,
                'available_themes_list': available_themes_list}

    def _get_themes_list(self):
        """回傳目前系統上的樣板名稱列表"""
        themes_dir =  get_project_abspath() / 'themes'
        return [theme.name for theme in themes_dir.glob('*') if theme.name != 'default']

    def _set_theme(theme_name):
        """設定系統樣板"""
        default_theme_dir = get_project_abspath() / 'themes' / 'default'
        new_theme = get_project_abspath() / 'themes' / theme_name
        if default_theme_dir.exists():
            default_theme_dir.unlink()
        default_theme_dir.symlink_to(new_theme)
        return True

    def _validate(self, post_data):
        """跟資料庫的 sys config 比對，除了驗證資料類型之外，只回傳需要更改的 config list

        Args:
            post_data: pyramid 的 request.POST
        Returns:
            回傳需要更新的 list
        """
        db_sys_config_list = DAL.get_sys_config_list().all()
        updated_config_list = []
        for key, value in post_data.items():
            if key.startswith('site_'):
                for each_config in db_sys_config_list:
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
        """更新系統設定，並且更換 default symlink 的樣板"""

        # TODO: 不要處理 maintenance mode
        updated_config_list = self._validate(self.request.POST)
        for config in updated_config_list:
            if config['name'] == 'site_theme':
                self._set_theme(config['value'])
                logger.info('系統樣板變更為 %s', config['value'])
                break
        if updated_config_list:
            DAL.update_sys_config_list(updated_config_list)
            self.request.session.flash('更新設定成功', 'success')
            return HTTPFound(location=self.request.current_route_url())
        else:
            self.request.session.flash('設定沒有異動', 'fail')
            return HTTPFound(location=self.request.current_route_url())
