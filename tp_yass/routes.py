def includeme(config):
    config.add_static_view('static', 'tp_yass:themes/default/static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('login', '/login')
