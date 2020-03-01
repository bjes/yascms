from datetime import datetime

from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound

from tp_yass.forms.backend.news import NewsForm
from tp_yass.dal import DAL
from tp_yass.helper import sanitize_input
from tp_yass.views.backend.helper import upload_attachment, delete_attachment


@view_defaults(route_name='backend_news_create', renderer='tp_yass:themes/default/backend/news_create.jinja2', permission='edit')
class NewsCreateView:
    """建立最新消息的 view"""

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get_view(self):
        """產生建立最新消息表單"""
        form = NewsForm()
        form.group_id.choices = [(each_staff_group.id, each_staff_group.name) for each_staff_group in
                                     DAL.get_staff_group_list(self.request.session['user_id'])]
        form.category_id.choices = [(category.id, category.name) for category in DAL.get_news_category_list()]
        return {'form': form}

    @view_config(request_method='POST')
    def post_view(self):
        """處理建立最新消息的表單"""
        form = NewsForm()
        form.group_id.choices = [(each_staff_group.id, each_staff_group.name) for each_staff_group in
                                 DAL.get_staff_group_list(self.request.session['user_id'])]
        form.category_id.choices = [(category.id, category.name) for category in DAL.get_news_category_list()]
        form.process(self.request.POST)
        if form.validate():
            created_news = DAL.create_news(form)
            # 先上傳檔案再將檔案相關資料寫入資料庫
            if form.attachments.data:
                for each_upload in form.attachments.data:
                    now = datetime.now()
                    saved_file_name = upload_attachment(each_upload, now.strftime('news/%Y/%m'), f'{created_news.id}_')
                    created_news.attachments.append(DAL.create_news_attachment(each_upload.filename, saved_file_name))
            DAL.save_news(created_news)
            return HTTPFound(self.request.route_url('backend_news_list'))
        return {'form': form}


@view_defaults(route_name='backend_news_list', renderer='themes/default/backend/news_list.jinja2', permission='view')
class NewsListView:
    """顯示最新消息列表的 view class"""

    def __init__(self, request):
        """
        Args:
            request: pyramid.request.Request
        """
        self.request = request

    @view_config(request_method='GET')
    def get_view(self):
        """顯示最新消息的列表"""
        quantity_per_page = sanitize_input(self.request.GET.get('q', 20), int, 20)
        category_id = sanitize_input(self.request.GET.get('c'), int, None)
        page_number = sanitize_input(self.request.GET.get('p', 1), int, 1)
        news_list = DAL.get_news_list(page_number=page_number, quantity_per_page=quantity_per_page, category_id=category_id)
        return {'news_list': news_list,
                'page_quantity_of_total_news': DAL.get_page_quantity_of_total_news(quantity_per_page, category_id),
                'page_number': page_number,
                'quantity_per_page': quantity_per_page}


@view_defaults(route_name='backend_news_delete',
               permission='edit')
class NewsDeleteView:
    """刪除最新消息，只有管理者與最新消息所屬群組可刪"""

    def __init__(self, request):
        """
        Args:
            request: pyramid.request.Request
        """
        self.request = request

    @view_config()
    def delete_view(self):
        """刪除指定的最新消息"""
        news_id = int(self.request.matchdict['news_id'])
        news = DAL.get_news(news_id)
        if news:
            for each_attachment in news.attachments:
                delete_attachment(each_attachment, news.publication_date.strftime('news/%Y/%m'))
            DAL.delete_news(news)
        return HTTPFound(self.request.route_url('backend_news_list'))
