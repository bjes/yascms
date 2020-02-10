import logging

from pyramid.security import (Allow,
                              Everyone,
                              ALL_PERMISSIONS)


logger = logging.getLogger(__name__)


class BaseResource:

    def __call__(self, request):
        self.request = request
        return self


class AuthUserResource(BaseResource):

    def __acl__(self):
        """只要有登入，不管是一般帳號還是管理者帳號，都會存在 groups 這個 session，直接給過
        """
        if 'groups' in self.request.session:
            logger.debug('比對群組權限接受，權限為已有帳號的身份')
            return [(Allow, Everyone, ALL_PERMISSIONS)]
        return []


class AdminResource(BaseResource):

    def __acl__(self):
        """Admin 的群組 type 為 0，所以給 group type 為 0 的群組權限全開"""
        if 'groups' in self.request.session:
            for each_group_tree in self.request.session['groups']:
                for each_group in each_group_tree:
                    if each_group['type'] == 0:
                        logger.debug('比對群組 %s 權限接受，權限為管理者', each_group)
                        return [(Allow, each_group['id'], ALL_PERMISSIONS)]
        return []
