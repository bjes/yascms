from pyramid.view import view_config, view_defaults

from yascms.dal import DAL
from yascms.helpers import sanitize_input
from yascms.enum import AuthLogType


@view_defaults(route_name='backend_auth_log_list', permission='view', renderer='')
class AuthLogListView:
    """顯示 auth log 列表的 view class"""

    def __init__(self, request):
        """
        Args:
            request: pyramid.request.Request
        """
        self.request = request
        self.request.override_renderer = f'themes/{request.effective_theme_name}/backend/auth_log_list.jinja2'

    @view_config(request_method='GET')
    def get_view(self):
        """顯示 auth log 的列表"""
        quantity_per_page = sanitize_input(self.request.GET.get('q', 20), int, 20)
        page_number = sanitize_input(self.request.GET.get('p', 1), int, 1)
        user_id = sanitize_input(self.request.GET.get('u', None), int, None)
        # 一般使用者只能看自己的 log，只有管理者可以看全部
        if not self.request.session['is_admin']:
            user_id = self.request.session['user_id']
        auth_log_list = DAL.get_auth_log_list(page_number, quantity_per_page, user_id)
        return {'auth_log_list': auth_log_list,
                'page_quantity_of_total_auth_logs': DAL.get_page_quantity_of_total_auth_logs(quantity_per_page, user_id),
                'page_number': page_number,
                'quantity_per_page': quantity_per_page,
                'AuthLogType': AuthLogType}
