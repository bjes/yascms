import pathlib
import subprocess

import pytest
from pyramid.testing import DummyRequest

import tp_yass


HERE = pathlib.Path(tp_yass.__file__).parent.parent
INI_FILE = HERE / 'development.ini'


def get_global_config():
    """產生 tp_yass.main 所需的 global_config 資料結構"""
    import collections

    global_config = collections.OrderedDict()
    global_config['here'] = str(HERE)
    global_config['__file__'] = str(INI_FILE)
    return global_config


@pytest.fixture(scope='session')
def ini_settings():
    """產生 tp_yass.main 所需的 settings 資料結構。但取得之前必須確保 development.ini 有存在，所以做檢查，
    若不存在，則用 soft link 建立測試用的檔案
    """
    from tp_yass.tests.helper import get_ini_settings

    if not INI_FILE.exists():
        if INI_FILE.is_symlink():
            INI_FILE.unlink()
        test_ini_file = pathlib.Path(__file__).parent / 'data/test_development.ini'
        INI_FILE.symlink_to(test_ini_file)
    return get_ini_settings(str(INI_FILE))


@pytest.fixture(scope='session')
def webtest_testapp(session_pyramid_config, ini_settings):
    """產生 webtest 物件以用來跑測試"""
    from webtest import TestApp
    from tp_yass import main

    return TestApp(main(get_global_config(), **ini_settings), extra_environ={'REMOTE_ADDR': '127.0.0.1'})


@pytest.fixture(scope='session')
def webtest_admin_testapp(webtest_testapp):
    """使用最高權限登入"""
    request = DummyRequest()
    response = webtest_testapp.get(request.route_path('login'))
    # 若已經登入成功，不會顯示登入表單，而會 redirect 到 backend
    if response.status_int != 302:
        form = response.form
        form['account'] = 'admin'
        form['password'] = 'admin4tp_yass'
        form.submit()
    return webtest_testapp


@pytest.fixture(autouse=True, scope='function')
def init_test_db():
    """自動初始化測試用資料"""
    subprocess.run(['inv', 'db.init-test'])
