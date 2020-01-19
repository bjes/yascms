from pyramid.events import NewRequest
from pyramid.events import subscriber

from tp_yass.dal import DAL

@subscriber(NewRequest)
def sysconfig(event):
    event.request.sysconfig = {config.name: config.value for config in DAL.get_sys_config()}
