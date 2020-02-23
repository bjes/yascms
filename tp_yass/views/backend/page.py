from pathlib import Path
from tempfile import NamedTemporaryFile

from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound

from tp_yass.forms.backend.page import PageForm
from tp_yass.helper import sanitize_input
from tp_yass.views.helper.file import get_static_abspath, save_file
from tp_yass.dal import DAL


@view_defaults(route_name='backend_page_create',
               renderer='themes/default/backend/page_create.jinja2',
               permission='edit')
class PageCreateView:
    """建立單一頁面的 view class"""

    def __init__(self, context, request):
        """
        Args:
            context: 因為頁面還未建立，所以 context 為管理者才有權限的 acl
            request: pyramid.request.Request
        """
        self.context = context
        self.request = request

    @view_config(request_method='GET')
    def get_view(self):
        """顯示新增單一頁面的網頁"""
        form = PageForm()
        return {'form': form}

    def _upload_attachment(self, cgi_field_storage, prefix):
        """將上傳的檔案重新亂數命名後存檔"""
        upload_file_name = Path(cgi_field_storage.filename)
        with NamedTemporaryFile(dir=str(get_static_abspath() / 'uploads' / 'pages'),
                                prefix=prefix,
                                suffix=upload_file_name.suffix) as destination_file:
            save_file(cgi_field_storage, destination_file)
            return str(Path(destination_file.name).name)

    @view_config(request_method='POST')
    def post_view(self):
        """新增單一頁面"""
        form = PageForm(self.request.POST)
        if form.validate():
            created_page = DAL.create_page(form)
            if form.attachments.data:
                for each_upload in form.attachments.data:
                    saved_file_name = self._upload_attachment(each_upload, f'{created_page.id}_')
                    created_page.attachments.append(DAL.create_page_attachment(each_upload.filename, saved_file_name))
            DAL.save_page(created_page)
            return HTTPFound(self.request.route_url('backend_page_list'))
        else:
            return {'form': form}


@view_defaults(route_name='backend_page_list',
               renderer='themes/default/backend/page_list.jinja2',
               permission='view')
class PageListView:
    """顯示單一頁面列表的 view class"""

    def __init__(self, context, request):
        """
        Args:
            context: context 為有註冊帳號才有權限的 acl
            request: pyramid.request.Request
        """
        self.context = context
        self.request = request

    @view_config(request_method='GET')
    def get_view(self):
        """顯示單一頁面的列表"""
        quantity_per_page = sanitize_input(self.request.GET.get('q', 20), int, 20)
        group_id = sanitize_input(self.request.GET.get('g'), int, None)
        page_id = sanitize_input(self.request.GET.get('p', 1), int, 1)
        page_list = DAL.get_page_list(page=page_id, group_id=group_id, quantity_per_page=quantity_per_page)
        return {'page_list': page_list,
                'page_quantity_of_total_pages': DAL.get_page_quantity_of_total_pages(quantity_per_page, group_id),
                'page_id': page_id,
                'quantity_per_page': quantity_per_page}
