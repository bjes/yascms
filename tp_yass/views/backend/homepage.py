from pyramid.view import view_config

from tp_yass.dal import DAL


@view_config(route_name='backend_homepage', renderer='', permission='view')
def backend_homepage_view(request):
    request.override_renderer = f'themes/{request.effective_theme_name}/backend/homepage.jinja2'

    return {'today_successful_auth_qty': DAL.get_today_successful_auth_qty(),
            'today_wrong_password_auth_qty': DAL.get_today_wrong_password_auth_qty(),
            'users_qty': DAL.get_users_qty(),
            'groups_qty': DAL.get_groups_qty(),
            'news_qty': DAL.get_news_qty(),
            'telext_qty': DAL.get_telext_qty(),
            'links_qty': DAL.get_links_qty()}
