import logging

from pyramid.security import (Allow,
                              Everyone,
                              ALL_PERMISSIONS)


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

