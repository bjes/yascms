from pyramid.view import view_config, view_defaults

from tp_yass.forms.backend.news import NewsForm
from tp_yass.dal import DAL


@view_defaults(route_name='backend_news_create', renderer='tp_yass:themes/default/backend/news_create.jinja2', permission='edit')
class NewsCreateView:
    """建立最新消息的 view"""

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get_view(self):
        """產生建立最新消息表單"""
        form = NewsForm()
        form.category_id.choices = [(category.id, category.name) for category in DAL.get_news_category_list()]
        return {'form': form}

    @view_config(request_method='POST')
    def post_view(self):
        """處理建立最新消息的表單"""
        form = NewsForm()
        form.category_id.choices = [(category.id, category.name) for category in DAL.get_news_category_list()]
        form.process(self.request.POST)
        if form.validate():
            import pdb; pdb.set_trace()
        return {'form': form}

