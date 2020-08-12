import logging

from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound

from tp_yass.enum import NavbarType
from tp_yass.views.helper.navbar import generate_navbar_trees
from tp_yass.forms.backend.navbar import NavbarForm, NavbarEditForm
from tp_yass.dal import DAL


logger = logging.getLogger(__name__)


@view_defaults(route_name='backend_navbar_list',
               renderer='themes/default/backend/navbar_list.jinja2',
               permission='view')
class NavbarListView:

    def __init__(self, request):
        self.request = request

    @view_config()
    def list_view(self):
        """後台顯示 navbar 樹狀結構"""
        return {'navbar_trees': generate_navbar_trees(self.request)}


@view_defaults(route_name='backend_navbar_create',
               renderer='themes/default/backend/navbar_create.jinja2',
               permission='edit')
class NavbarCreateView:
    """建立巢狀選單"""

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get_view(self):
        form = NavbarForm()
        return {'form': form, 'navbar_trees': generate_navbar_trees(self.request, type='intermediate')}

    @view_config(request_method='POST')
    def post_view(self):
        form = NavbarForm(self.request.POST)
        if form.validate():
            if DAL.create_navbar(form):
                return HTTPFound(self.request.route_url('backend_navbar_list'))
        return {'form': form,
                'navbar_trees': generate_navbar_trees(self.request, type='intermediate'),
                'NavbarType': NavbarType}


@view_defaults(route_name='backend_navbar_delete', permission='edit')
class NavbarDeleteView:
    """刪除 navbar 與其下面的所有選單"""

    def __init__(self, request):
        self.request = request

    def _recursive_delete(self, navbar):
        """遞迴刪除整串導覽列"""
        if navbar.descendants:
            for each_sub_navbar in navbar.descendants:
                result = self._recursive_delete(each_sub_navbar)
                if not result:
                    return False
        else:
            return DAL.delete_navbar(navbar)

    @view_config()
    def delete_view(self):
        """將整串導覽列刪除"""
        # TODO: 要做成讓使用者決定要整串刪掉還是孤兒的節點都搬移至未指定
        navbar_id = int(self.request.matchdict['navbar_id'])
        navbar = DAL.get_navbar(navbar_id)
        if navbar:
            if not self._recursive_delete(navbar):
                self.request.session.flash('刪除導覽列失敗，請確認導覽列類型是否正確', 'fail')
        return HTTPFound(self.request.route_url('backend_navbar_list'))



@view_defaults(route_name='backend_navbar_edit',
               renderer='themes/default/backend/navbar_edit.jinja2',
               permission='edit')
class NavbarEditView:

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get_view(self):
        navbar_id = int(self.request.matchdict['navbar_id'])
        navbar = DAL.get_navbar(navbar_id)

        form = NavbarEditForm(name=navbar.name,
                              type=navbar.type,
                              aria_name=navbar.aria_name,
                              url=navbar.url,
                              icon=navbar.icon,
                              order=navbar.order)
        if navbar.page:
            form.leaf_type.data = 1
            form.page_id.data = navbar.page.id
        else:
            form.leaf_type.data = 2
        form.is_external.data = True if navbar.is_external else False
        form.is_visible.data = True if navbar.is_visible else False
        if navbar.ancestor:
            form.ancestor_id.data = navbar.ancestor.id
        return {'form': form,
                'navbar_trees': generate_navbar_trees(self.request, type='intermediate', excluded_id=navbar_id),
                'NavbarType': NavbarType}

    @view_config(request_method='POST')
    def post_view(self):
        navbar_id = int(self.request.matchdict['navbar_id'])
        navbar = DAL.get_navbar(navbar_id)
        if navbar:
            form = NavbarEditForm(self.request.POST)
            if form.validate():
                if DAL.sync_navbar(form, navbar):
                    return HTTPFound(self.request.route_url('backend_navbar_list'))
        self.request.session.flash('navbar id 不存在', 'fail')
        return {'form': form,
                'navbar_trees': generate_navbar_trees(self.request, type='intermediate', excluded_id=navbar_id),
                'NavbarType': NavbarType}
