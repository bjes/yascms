import secrets

from yascms.dal import DAL


def get_site_config(request):
    return {config.name: config.value for config in DAL.get_site_config_list()}


def get_current_theme_name(request):
    return DAL.get_current_theme_name()


def get_current_theme_config(request):
    return DAL.get_theme_config(request.current_theme_name)


def get_banner(request):
    banner_name = secrets.choice(request.current_theme_config['settings']['banners']['value'])
    return request.static_url(f'yascms:uploads/themes/{request.current_theme_name}/banners/{banner_name}')


def get_effective_theme_name(request):
    """實作管理者才可以 preview 不同的樣板，透過 GET 傳入參數 override_theme_name
    動態改變 request.effective_theme_name 的值
    """
    if (request.session.get('is_admin', False) and
        request.GET.get('override_theme_name', None) in DAL.get_available_theme_name_list()):
        return request.GET['override_theme_name']
    else:
        return request.current_theme_name


def get_effective_theme_config(request):
    """實作管理者才可以 preview 不同的樣板，透過 GET 傳入參數 override_theme_name
    動態改變 request.effective_theme_config 的值
    """
    if (request.session.get('is_admin', False) and
        request.GET.get('override_theme_name', None) in DAL.get_available_theme_name_list()):
        return DAL.get_theme_config(request.GET['override_theme_name'])
    else:
        return request.current_theme_config


def includeme(config):
    config.add_request_method(get_site_config, 'site_config', reify=True)
    config.add_request_method(get_current_theme_name, 'current_theme_name', reify=True)
    config.add_request_method(get_current_theme_config, 'current_theme_config', reify=True)
    config.add_request_method(get_effective_theme_name, 'effective_theme_name', reify=True)
    config.add_request_method(get_effective_theme_config, 'effective_theme_config', reify=True)
    config.add_request_method(get_banner, 'banner', reify=True)


