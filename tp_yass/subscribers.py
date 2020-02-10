from pyramid.events import NewRequest
from pyramid.events import subscriber

from tp_yass.dal import DAL


@subscriber(NewRequest)
def sysconfig(event):
    """為避免不必要的權限檢查造成過多的資料庫存取，採用 event 在每次 request 時將 sysconfig 存入 request 下"""
    event.request.sysconfig = {config.name: config.value for config in DAL.get_sys_config_list()}
