import random

from pyramid.events import NewRequest, subscriber

from tp_yass.dal import DAL


@subscriber(NewRequest)
def load_config(event):
    """為避免不必要的權限檢查造成過多的資料庫存取，
    採用 event 在每次 request 時將 global_config / current_theme_name / current_theme_config 存入 request 下。
    其中 event.request.cache 是在初始化專案時透過 add_request_method 加進來的。
    """
    event.request.global_config = event.request.cache.get_global_config()

    # 為了實作可以 preview 不同的樣板，透過 GET 傳入參數 override_theme_name 用來動態改變 request.current_theme 的值
    if (event.request.session.get('is_admin', False) and
        event.request.GET.get('override_theme_name', None) in event.request.cache.get_available_theme_name_list()):

        current_theme_name = event.request.GET['override_theme_name']
        event.request.current_theme_name = current_theme_name
        event.request.current_theme_config = DAL.get_theme_config(current_theme_name)
    else:
        event.request.current_theme_name = event.request.cache.get_current_theme_name()
        event.request.current_theme_config = event.request.cache.get_current_theme_config()

    if not event.request.path.startswith('/backend'):
        banner_name = random.choice(event.request.current_theme_config['settings']['banners']['value'])
        event.request.banner = event.request.static_url(f'tp_yass:uploads/themes/{event.request.current_theme_name}/banners/{banner_name}')
