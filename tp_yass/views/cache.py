import pickle

import redis

from tp_yass.dal import DAL


class CacheController:

    def __init__(self, redis_url, prefix):
        self.redis = redis.Redis.from_url(redis_url)
        self.prefix = prefix

    def __call__(self, request):
        return self

    def get_site_config(self):
        key = f'{self.prefix}_site_config'
        cache = self.redis.get(key)
        if cache:
            return pickle.loads(cache)
        else:
            config = {config.name: config.value for config in DAL.get_site_config_list()}
            self.redis.set(key, pickle.dumps(config))
            return config

    def delete_site_config(self):
        self.redis.delete(f'{self.prefix}_site_config')
        return True

    def get_theme_config(self, theme_name):
        key = f'{self.prefix}_theme_config'
        cache = self.redis.get(key)
        if cache:
            return pickle.loads(cache)
        else:
            config = DAL.get_theme_config(theme_name)
            self.redis.set(key, pickle.dumps(config))
            return config

    def delete_theme_config(self):
        self.redis.delete(f'{self.prefix}_theme_config')
        return True

    def get_current_theme(self):
        key = f'{self.prefix}_current_theme'
        cache = self.redis.get(key)
        if cache:
            return cache.decode('utf8')
        else:
            current_theme = DAL.get_current_theme()
            self.redis.set(key, current_theme)
            return current_theme
