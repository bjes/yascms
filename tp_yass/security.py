from pyramid.authentication import SessionAuthenticationHelper
from pyramid.authorization import ACLHelper, Everyone


class SecurityPolicy:
    """實作 pyramid 2.0 之後引入的 security framework"""

    def __init__(self):
        self.helper = SessionAuthenticationHelper()
        self.acl = ACLHelper()

    def identity(self, request):
        identity = self.helper.authenticated_userid(request)
        if identity == request.session.get('user_id'):
            return identity

    def authenticated_userid(self, request):
        identity = self.identity(request)
        if identity is not None:
            return identity

    def permits(self, request, context, permission):
        """進行 authorization 驗證"""
        principals = self.effective_principals(request)
        return self.acl.permits(context, principals, permission)

    def effective_principals(self, request):
        """回傳此使用者的群組列表，所謂的 principals 可以理解為這個使用者所屬的群組 list。
        
        這邊會有 Everyone 這個 principal 原因是我們有些 acl 判斷會直接對 Everyone。詳情可以看 resources.py"""
        return [Everyone] + list(request.session.get('group_id_list', set()))

    def remember(self, request, userid, **kw):
        return self.helper.remember(request, userid, **kw)

    def forget(self, request, **kw):
        return self.helper.forget(request, **kw)

