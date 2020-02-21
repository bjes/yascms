import logging

from pyramid.security import (Allow,
                              Everyone,
                              ALL_PERMISSIONS)

from tp_yass.helper import sanitize_input
from tp_yass.dal import DAL


logger = logging.getLogger(__name__)


class ACL:
    pass


def admin_factory(request):
    """Admin 的群組 type 為 0，所以給 group type 為 0 的群組權限全開

    只要有一個群組為 admin，則 acl 就設定對於該 group id 權限全開
    """
    acl = ACL()
    if 'is_admin' in request.session and request.session['is_admin']:
        acl.__acl__ = [(Allow, Everyone, ALL_PERMISSIONS)]
    else:
        acl.__acl__ = []
    return acl


def auth_user_factory(request):
    """只要有登入，不管是一般帳號還是管理者帳號，都會存在 groups 這個 session，直接給過"""
    acl = ACL()
    if 'groups' in request.session:
        logger.debug('比對群組權限接受，權限為已有帳號的身份')
        acl.__acl__ = [(Allow, Everyone, ALL_PERMISSIONS)]
    else:
        acl.__acl__ = []
    return acl


def get_page_factory(request):
    """單一頁面所屬的群組（們）才有後台編輯的權限"""
    acl = ACL()
    page_id = sanitize_input(request.GET.get('id'), int, None)
    if page_id:
        page = DAL.get_page(page_id)
        # 若為管理者，權限全開
        if 'is_admin' in request.session and request.session['is_admin']:
            page.__acl__ = [(Allow, Everyone, ALL_PERMISSIONS)]
        # 否則只有 page 的群組有 edit 權限
        else:
            for each_group in page.groups:
                page.__acl__.append((Allow, each_group.id, 'edit'))
    else:
        acl.__acl__ = []
    return page or acl
