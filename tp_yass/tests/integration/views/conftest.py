import pathlib
import subprocess

import pytest

import tp_yass


HERE = pathlib.Path(tp_yass.__file__).parent.parent
INI_FILE = HERE / 'development.ini'


def get_global_config():
    import collections
    """產生 tp_yass.main 所需的 global_config 資料結構"""
    global_config = collections.OrderedDict()
    global_config['here'] = str(HERE)
    global_config['__file__'] = str(INI_FILE)
    return global_config


def get_settings():
    """產生 tp_yass.main 所需的 settings 資料結構"""
    from tp_yass.tests.helper import get_ini_settings
    return get_ini_settings(str(INI_FILE))


@pytest.fixture
def webtest_testapp(pyramid_config):
    """產生 webtest 物件以用來跑測試"""
    from webtest import TestApp
    from tp_yass import main

    return TestApp(main(get_global_config(), **get_settings()))


@pytest.fixture
def webtest_admin_testapp(webtest_testapp):
    """使用最高權限登入"""
    response = webtest_testapp.get(request.route_path('login'))
    form = response.form
    form['account'] = 'admin'
    form['password'] = 'admin4tp_yass'
    form.submit()
    return webtest_testapp


@pytest.fixture(autouse=True)
def init_test_db():
    """自動初始化測試用資料"""
    subprocess.run(['inv', 'db.init-test'])


@pytest.fixture(autouse=True)
def init_ini_file(shared_datadir):
    """在每次跑 integration tests 前檢查 development.ini 是否存在，
    若否，用 soft link 建立測試用的檔案
    """
    if not INI_FILE.exists():
        test_ini_file = shared_datadir / 'test_development.ini'
        INI_FILE.symlink_to(test_ini_file)


@pytest.fixture(autouse=True, scope='session')
def init_sqlalchemy():
    from sqlalchemy import create_engine
    from pyramid_sqlalchemy import init_sqlalchemy

    ini_settings = get_settings()
    init_sqlalchemy(create_engine(ini_settings['sqlalchemy.url']))

