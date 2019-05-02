from pyramid.security import Allow, ALL_PERMISSIONS

class Resource:

    def __call__(self, request):
        self.request = request
        return self

    def __acl__(self):
        return [(Allow, 'manager', 'edit'),
                (Allow, 'users', 'view'),
                (Allow, 'admin', ALL_PERMISSIONS)]

