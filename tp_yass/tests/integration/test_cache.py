import pickle

import redis
from pyramid.testing import DummyRequest

from tp_yass.cache import CacheController


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


def test_get_current_theme_config_should_return_config(ini_settings, init_db_session):
    test_prefix = 'test'
    theme_name = 'tp_yass2020'

    redis_instance = get_redis(ini_settings['redis.sessions.url'])
    redis_instance.delete(f'{test_prefix}_current_theme_config')

    request = DummyRequest()
    cache = CacheController(ini_settings['redis.sessions.url'], test_prefix)
    assert cache(request).get_current_theme_config()
    assert redis_instance.get(f'{test_prefix}_current_theme_config')


def test_delete_current_theme_config_should_delete_config(ini_settings, init_db_session):
    test_prefix = 'test'

    redis_instance = get_redis(ini_settings['redis.sessions.url'])
    redis_instance.set(f'{test_prefix}_current_theme_config', 'foo')

    request = DummyRequest()
    cache = CacheController(ini_settings['redis.sessions.url'], test_prefix)

    assert cache(request).delete_current_theme_config()
    assert not redis_instance.exists(f'{test_prefix}_current_theme_config')


def test_get_current_theme_name_should_return_current_theme_name(ini_settings, init_db_session):
    test_prefix = 'test'

    redis_instance = get_redis(ini_settings['redis.sessions.url'])
    redis_instance.delete(f'{test_prefix}_current_theme_name')

    request = DummyRequest()
    cache = CacheController(ini_settings['redis.sessions.url'], test_prefix)
    theme_name = cache(request).get_current_theme_name()
    assert theme_name
    assert redis_instance.get(f'{test_prefix}_current_theme_name').decode('utf8') == theme_name


def test_delete_current_theme_name_should_delete_current_theme_cache(ini_settings, init_db_session):
    test_prefix = 'test'

    redis_instance = get_redis(ini_settings['redis.sessions.url'])
    redis_instance.set(f'{test_prefix}_current_theme_name', 'foo')

    request = DummyRequest()
    cache = CacheController(ini_settings['redis.sessions.url'], test_prefix)

    assert cache(request).delete_current_theme_name()
    assert not redis_instance.exists(f'{test_prefix}_current_theme_name')


def test_get_available_theme_name_list_should_return_available_themes_list(ini_settings, init_db_session):
    test_prefix = 'test'

    redis_instance = get_redis(ini_settings['redis.sessions.url'])
    redis_instance.delete(f'{test_prefix}_available_theme_name_list')

    request = DummyRequest()
    cache = CacheController(ini_settings['redis.sessions.url'], test_prefix)
    available_thems = cache(request).get_available_theme_name_list()
    assert available_thems
    assert pickle.loads(redis_instance.get(f'{test_prefix}_available_theme_name_list')) == available_thems


def test_delete_available_themes_should_delete_available_themes_cache(ini_settings, init_db_session):
    test_prefix = 'test'

    redis_instance = get_redis(ini_settings['redis.sessions.url'])
    redis_instance.set(f'{test_prefix}_available_theme_name_list', 'foo')

    request = DummyRequest()
    cache = CacheController(ini_settings['redis.sessions.url'], test_prefix)

    assert cache(request).delete_available_theme_name_list()
    assert not redis_instance.exists(f'{test_prefix}_available_theme_name_list')
