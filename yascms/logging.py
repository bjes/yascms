import json
import logging

import requests


class MattermostHandler(logging.Handler):

    def __init__(self, channel_name, channel_url):
        super().__init__()
        self.channel_name = channel_name
        self.channel_url = channel_url

    def emit(self, record):
        log_entry = self.format(record)
        payload = {'text': log_entry,
                   'channel': self.channel_name}
        return requests.post(self.channel_url,
                             json.dumps(payload),
                             headers={'Content-type': 'application/json'}).content
