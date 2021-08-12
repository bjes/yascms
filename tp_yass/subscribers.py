import random

from pyramid.events import NewRequest, subscriber

from tp_yass.dal import DAL


@subscriber(NewRequest)
def load_config(event):
    """為避免不必要的權限檢查造成過多的資料庫存取，
    採用 event 在每次 request 時將 site_config / current_theme / theme_config 存入 request 下。
    其中 event.request.cache 是在初始化專案時透過 add_request_method 加進來的。
    """
    event.request.site_config = event.request.cache.get_site_config()
    event.request.current_theme = event.request.cache.get_current_theme()

    # 只有非後台的 url 才需要撈出佈景主題的設定檔置於 request 裡
    if not event.request.path.startswith('/backend'):
        event.request.theme_config = event.request.cache.get_theme_config(event.request.current_theme)
        banner_name = random.choice(event.request.theme_config['settings']['banners']['value'])
        event.request.banner = event.request.static_url(f'tp_yass:uploads/themes/{event.request.current_theme}/banners/{banner_name}')
