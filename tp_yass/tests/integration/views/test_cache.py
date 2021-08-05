import redis
from pyramid.testing import DummyRequest

from tp_yass.views.cache import CacheController


def get_redis(redis_url):
    return redis.Redis.from_url(redis_url)


def test_get_site_config_should_return_config(ini_settings, init_db_session):
    test_prefix = 'test'

    redis_instance = get_redis(ini_settings['redis.sessions.url'])
    redis_instance.delete(f'{test_prefix}_site_config')

    request = DummyRequest()
    cache = CacheController(ini_settings['redis.sessions.url'], test_prefix)
    assert cache(request).get_site_config()
    assert redis_instance.get(f'{test_prefix}_site_config')


def test_delete_site_config_should_delete_config(ini_settings, init_db_session):
    test_prefix = 'test'

    redis_instance = get_redis(ini_settings['redis.sessions.url'])
    redis_instance.set(f'{test_prefix}_site_config', 'foo')

    request = DummyRequest()
    cache = CacheController(ini_settings['redis.sessions.url'], test_prefix)

    assert cache(request).delete_site_config()
    assert not redis_instance.exists(f'{test_prefix}_site_config')


def test_get_theme_config_should_return_config(ini_settings, init_db_session):
    test_prefix = 'test'
    theme_name = 'tp_yass2020'

    redis_instance = get_redis(ini_settings['redis.sessions.url'])
    redis_instance.delete(f'{test_prefix}_theme_config')

    request = DummyRequest()
    cache = CacheController(ini_settings['redis.sessions.url'], test_prefix)
    assert cache(request).get_theme_config(theme_name)
    assert redis_instance.get(f'{test_prefix}_theme_config')


def test_delete_theme_config_should_delete_config(ini_settings, init_db_session):
    test_prefix = 'test'

    redis_instance = get_redis(ini_settings['redis.sessions.url'])
    redis_instance.set(f'{test_prefix}_theme_config', 'foo')

    request = DummyRequest()
    cache = CacheController(ini_settings['redis.sessions.url'], test_prefix)

    assert cache(request).delete_theme_config()
    assert not redis_instance.exists(f'{test_prefix}_theme_config')


def test_get_current_theme_should_return_current_theme_name(ini_settings, init_db_session):
    test_prefix = 'test'

    redis_instance = get_redis(ini_settings['redis.sessions.url'])
    redis_instance.delete(f'{test_prefix}_theme_name')

    request = DummyRequest()
    cache = CacheController(ini_settings['redis.sessions.url'], test_prefix)
    theme_name = cache(request).get_current_theme()
    assert theme_name
    assert redis_instance.get(f'{test_prefix}_current_theme').decode('utf8') == theme_name
