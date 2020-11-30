from pyramid.events import NewRequest
from pyramid.events import subscriber

from tp_yass.dal import DAL


@subscriber(NewRequest)
def load_config(event):
    """為避免不必要的權限檢查造成過多的資料庫存取，
    採用 event 在每次 request 時將 site_config 與 theme_config 存入 request 下
    """
    site_config = {config.name: config.value for config in DAL.get_site_config_list()}
    event.request.site_config = site_config
    # 只有非後台的 url 才需要撈出佈景主題的設定檔置於 request 裡
    if not event.request.path.startswith('/backend'):
        event.request.theme_config = DAL.get_theme_config(site_config['site_theme'])
