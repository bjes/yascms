from .resources import (auth_user_factory,
                        admin_factory,
                        page_edit_factory,
                        staff_group_factory,
                        news_edit_factory,
                        link_edit_factory)

def includeme(config):

    # frontend
    config.add_route('homepage', '/')
    config.add_route('news_list', '/news/list')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    # backend
    config.add_route('backend_homepage', '/backend/', factory=auth_user_factory)

    config.add_route('backend_sys_config_edit', '/backend/sys/config/edit', factory=admin_factory)

    config.add_route('backend_navbar_create', '/backend/navbar/create', factory=admin_factory)
    config.add_route('backend_navbar_list', '/backend/navbar/list', factory=admin_factory)
    config.add_route('backend_navbar_delete', '/backend/navbar/delete/{navbar_id:\d+}', factory=admin_factory)
    config.add_route('backend_navbar_edit', '/backend/navbar/edit/{navbar_id:\d+}', factory=admin_factory)

    config.add_route('backend_user_list', '/backend/user/list', factory=admin_factory)

    config.add_route('backend_user_group_create', '/backend/user/group/create', factory=admin_factory)
    config.add_route('backend_user_group_list', '/backend/user/group/list', factory=admin_factory)
    config.add_route('backend_user_group_delete', '/backend/user/group/delete/{group_id:\d+}', factory=admin_factory)
    config.add_route('backend_user_group_edit', '/backend/user/group/edit/{group_id:\d+}', factory=admin_factory)

    config.add_route('backend_page_create', '/backend/page/create', factory=admin_factory)
    config.add_route('backend_page_list', '/backend/page/list', factory=auth_user_factory)
    config.add_route('backend_page_delete', '/backend/page/delete/{page_id:\d+}', factory=admin_factory)
    config.add_route('backend_page_edit', '/backend/page/edit/{page_id:\d+}', factory=page_edit_factory)

    config.add_route('backend_news_create', '/backend/news/create', factory=staff_group_factory)
    config.add_route('backend_news_list', '/backend/news/list', factory=auth_user_factory)
    config.add_route('backend_news_delete', '/backend/news/delete/{news_id:\d+}', factory=news_edit_factory)
    config.add_route('backend_news_edit', '/backend/news/edit/{news_id:\d+}', factory=news_edit_factory)

    config.add_route('backend_news_category_create', '/backend/news/category/create', factory=admin_factory)
    config.add_route('backend_news_category_list', '/backend/news/category/list', factory=admin_factory)
    config.add_route('backend_news_category_delete', '/backend/news/category/delete/{news_category_id:\d+}', factory=admin_factory)
    config.add_route('backend_news_category_edit', '/backend/news/category/edit/{news_category_id:\d+}', factory=admin_factory)

    config.add_route('backend_link_create', '/backend/link/create', factory=staff_group_factory)
    config.add_route('backend_link_list', '/backend/link/list', factory=staff_group_factory)
    config.add_route('backend_link_delete', '/backend/link/delete/{link_id:\d+}',
                     factory=link_edit_factory)
    config.add_route('backend_link_edit', '/backend/link/edit/{link_id:\d+}',
                     factory=link_edit_factory)

    config.add_route('backend_link_category_create', '/backend/link/category/create', factory=admin_factory)
    config.add_route('backend_link_category_list', '/backend/link/category/list', factory=admin_factory)
    config.add_route('backend_link_category_delete', '/backend/link/category/delete/{link_category_id:\d+}',
                     factory=admin_factory)
    config.add_route('backend_link_category_edit', '/backend/link/category/edit/{link_category_id:\d+}',
                     factory=admin_factory)

    config.add_route('backend_telext_create', '/backend/telext/create', factory=admin_factory)
    config.add_route('backend_telext_list', '/backend/telext/list', factory=admin_factory)
    config.add_route('backend_telext_delete', '/backend/telext/delete/{telext_id:\d+}', factory=admin_factory)
    config.add_route('backend_telext_edit', '/backend/telext/edit/{telext_id:\d+}', factory=admin_factory)

    # 開發用，上線環境會讓前端的 web server 處理這部份
    config.add_static_view('css', 'themes/default/static/css', cache_max_age=3600)
    config.add_static_view('js', 'themes/default/static/js', cache_max_age=3600)
    config.add_static_view('img', 'themes/default/static/img', cache_max_age=3600)
    config.add_static_view('uploads', 'uploads', cache_max_age=3600)
    config.add_static_view('', 'icons', cache_max_age=3600)
