from pyramid.view import (notfound_view_config,
                          forbidden_view_config)


@notfound_view_config(renderer='themes/default/404.jinja2', append_slash=True)
def notfound_view(request):
    request.response.status = 404
    return {}


@forbidden_view_config(renderer='themes/default/403.jinja2')
def forbidden_view(request):
    request.response.status = 403
    return {}
