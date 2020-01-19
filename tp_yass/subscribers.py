from pyramid.events import NewRequest
from pyramid.events import subscriber
from pyramid.httpexceptions import HTTPServiceUnavailable

from tp_yass.dal import DAL

@subscriber(NewRequest)
def sysconfig(event):
    event.request.sysconfig = {config.name: config.value for config in DAL.get_sys_config()}
    if event.request.sysconfig['maintenance_mode'] != 'false':
        raise HTTPServiceUnavailable('唯讀模式啟用中。')
