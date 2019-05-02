groups = {'admin': ['admin', 'manager'],
          'johndoe': ['users']}


def group_finder(user_name, request):
    username = request.GET.get('username', None)
    if username in groups:
        return groups[username]
    else:
        return None
