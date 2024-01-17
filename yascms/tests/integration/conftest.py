import os
import shutil
import pathlib
import collections
import subprocess

import pytest
from pyramid.testing import DummyRequest
from sqlalchemy import create_engine
from pyramid_sqlalchemy import init_sqlalchemy
from pyramid_sqlalchemy import Session as DBSession
from webtest import TestApp

import yascms
from yascms import main


HERE = pathlib.Path(yascms.__file__).parent.parent
INI_FILE = HERE / 'development.ini'


@pytest.fixture(scope='session')
def ini_settings():
    """產生 yascms.main 所需的 settings 資料結構。但取得之前必須確保 development.ini 有存在，所以做檢查，
    若不存在，則用 soft link 建立測試用的檔案
    """
    from yascms.tests.helper import get_ini_settings

    if not INI_FILE.exists():
        if INI_FILE.is_symlink():
            INI_FILE.unlink()
        test_ini_file = pathlib.Path(__file__).parent / 'data/test_development.ini'
        INI_FILE.symlink_to(test_ini_file)
    return get_ini_settings(str(INI_FILE))


@pytest.fixture
def init_db_session(ini_settings):
    """建立 sqlalchemy connection 以利測試可正常使用 orm，最後的 remove() 一定要呼叫
    不然會遇到重建資料庫時卡住的狀況"""
    engine = create_engine(ini_settings['sqlalchemy.url'])
    init_sqlalchemy(engine)
    yield
    DBSession.remove()


@pytest.fixture
def webtest_testapp(pyramid_config, ini_settings):
    """產生 webtest 物件以用來跑測試"""

    init_test_data()

    global_config = collections.OrderedDict()
    global_config['here'] = str(HERE)
    global_config['__file__'] = str(INI_FILE)

    yield TestApp(main(global_config, **ini_settings), extra_environ={'REMOTE_ADDR': '127.0.0.1'})

    DBSession.remove()


@pytest.fixture
def webtest_admin_testapp(webtest_testapp):
    """使用最高權限登入"""
    request = DummyRequest()
    response = webtest_testapp.get(request.route_path('login'))
    # 若已經登入成功，不會顯示登入表單，而會 redirect 到 backend
    if response.status_int != 302:
        form = response.form
        form['account'] = 'admin'
        form['password'] = 'admin4yascms'
        form.submit()
    yield webtest_testapp


def init_test_data():
    """自動初始化測試用資料"""
    cwd = os.getcwd()
    os.chdir(HERE)
    for each_theme in pathlib.Path(HERE / 'yascms/uploads/themes/').glob('*'):
        if each_theme.name != 'yascms2020':
            shutil.rmtree(each_theme)
    for each_item in pathlib.Path(HERE / 'yascms/themes/').glob('*'):
        if each_item.name != 'yascms2020':
            if each_item.is_dir():
                shutil.rmtree(each_item)
            else:
                each_item.unlink()
    for each_theme in pathlib.Path(HERE / 'yascms/static/').glob('*'):
        if (each_theme.name != 'yascms2020') and (not each_theme.name.startswith('.')):
            each_theme.unlink()
    for each_banner in pathlib.Path(HERE / 'yascms/uploads/themes/yascms2020/banners/').glob('*'):
        each_banner.unlink()
    subprocess.run(['inv', 'db.delete', 'file.delete', 'db.import-test-data'])
    os.chdir(cwd)
