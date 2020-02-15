from .resources import (AdminResource,
                        AuthUserResource)

def includeme(config):
    config.add_static_view('static', 'tp_yass:themes/default/static', cache_max_age=3600)

    # frontend
    config.add_route('homepage', '/')
    config.add_route('news_list', '/news/list')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    # backend
    config.add_route('backend_homepage', '/backend/', factory=AuthUserResource())
    config.add_route('backend_sys_config_edit', '/backend/sys/config/edit', factory=AuthUserResource())
    config.add_route('backend_navbar_list', '/backend/navbar/list', factory=AdminResource())
    config.add_route('backend_user_group_list', '/backend/user/group/list', factory=AdminResource())
