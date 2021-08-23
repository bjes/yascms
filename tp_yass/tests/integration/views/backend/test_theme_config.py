import pathlib

from pyramid.testing import DummyRequest
from webtest import Upload

from tp_yass.helpers import get_project_abspath
from tp_yass.dal import DAL


def test_theme_config_list(webtest_admin_testapp):
    request = DummyRequest()

    response = webtest_admin_testapp.get(request.route_path('backend_theme_config_list'))
    assert response.status_int == 200
    assert 'tp_yass2020' in response.body.decode('utf8')


def test_theme_config_general_edit_view(webtest_admin_testapp):
    request = DummyRequest()

    response = webtest_admin_testapp.get(request.route_path('backend_theme_config_general_edit',
                                                            theme_name='tp_yass2020'))
    assert response.status_int == 200
    assert '一般設定' in response.body.decode('utf8')

    form = response.form
    # 會 redirect 回 request.route_url('backend_theme_config_list')
    response = form.submit()
    assert response.status_int == 302
    assert request.route_path('backend_theme_config_list') in response.location


def test_theme_config_banners_edit_view(webtest_admin_testapp):
    request = DummyRequest()

    response = webtest_admin_testapp.get(request.route_path('backend_theme_config_banners_edit',
                                                            theme_name='tp_yass2020'))
    form = response.form
    # 一開始先全部 5 個橫幅都勾選，以便下面的測試
    for i in range(5):
        form[f'banners-{i}-is_visible'] = False
    form.submit()

    response = webtest_admin_testapp.get(request.route_path('backend_theme_config_banners_edit',
                                                            theme_name='tp_yass2020'))
    assert response.status_int == 200
    assert '橫幅設定' in response.body.decode('utf8')
    assert response.body.decode('utf8').count('checked') == 5  # tp_yass 預設的設定檔啟用的橫幅有 5 個

    form = response.form

    # 取消 4 個勾選
    for i in range(4):
        form[f'banners-{i}-is_visible'] = False
    # 會 redirect 回 request.route_url('backend_theme_config_list')
    response = form.submit()
    assert response.status_int == 302
    assert request.route_path('backend_theme_config_list') in response.location

    # 現在應該只剩 1 個有勾選
    response = webtest_admin_testapp.get(request.route_path('backend_theme_config_banners_edit',
                                                            theme_name='tp_yass2020'))
    assert response.status_int == 200
    assert response.body.decode('utf8').count('checked') == 1  # 勾選剩 1 個

    # 取消最後 1 個勾選會失敗，因為至少要勾選 1 個橫幅
    form = response.form
    form['banners-4-is_visible'] = False
    response = form.submit()
    assert 'alert-danger' in response.body.decode('utf8')  # 顯示 form validation 的 block


def test_theme_config_banners_upload_view(webtest_admin_testapp):
    request = DummyRequest()
    response = webtest_admin_testapp.get(request.route_path('backend_theme_config_banners_edit',
                                                             theme_name='tp_yass2020'))
    form_check_count = response.body.decode('utf8').count('form-check-input')

    response = webtest_admin_testapp.get(request.route_path('backend_theme_config_banners_upload',
                                                            theme_name='tp_yass2020'))
    test_banner_file_name = 'test_banner.jpg'
    form = response.form
    form['banners'] = Upload(test_banner_file_name, b'')
    response = form.submit()
    assert response.status_int == 302

    response = webtest_admin_testapp.get(request.route_path('backend_theme_config_banners_edit',
                                                            theme_name='tp_yass2020'))
    assert response.body.decode('utf8').count('form-check-input') == form_check_count + 1


def test_theme_config_banners_delete_view(webtest_admin_testapp):
    banner_name = 'banner01.jpg'
    theme_name = 'tp_yass2020'
    request = DummyRequest()
    banner_path = pathlib.Path(get_project_abspath()) / f'uploads/themes/{theme_name}/banners/{banner_name}'
    assert banner_path.exists()

    response = webtest_admin_testapp.get(request.route_path('backend_theme_config_banners_delete',
                                                            theme_name=theme_name, banner_name=banner_name))
    assert response.status_int == 302
    assert not banner_path.exists()


def test_theme_config_upload_and_activate_and_delete_view(webtest_admin_testapp, datadir):
    request = DummyRequest()
    response = webtest_admin_testapp.get(request.route_path('backend_theme_config_list'))
    theme_count = response.body.decode('utf8').count('一般設定')

    response = webtest_admin_testapp.get(request.route_path('backend_theme_config_upload'))
    test_theme_name = 'test_theme'
    test_theme_file_name = f'{test_theme_name}.zip'
    form = response.form
    form['theme'] = Upload(test_theme_file_name, open(datadir / test_theme_file_name, 'rb').read())
    response = form.submit()
    assert response.status_int == 302

    response = webtest_admin_testapp.get(request.route_path('backend_theme_config_list'))
    assert response.body.decode('utf8').count('一般設定') == theme_count + 1

    assert DAL.get_current_theme_name() == 'tp_yass2020'
    response = webtest_admin_testapp.get(request.route_path('backend_theme_config_activate',
                                                            theme_name=test_theme_name))
    assert response.status_int == 302
    assert DAL.get_current_theme_name() == test_theme_name

    response = webtest_admin_testapp.get(request.route_path('backend_theme_config_activate',
                                                            theme_name='tp_yass2020'))
    response = webtest_admin_testapp.get(request.route_path('backend_theme_config_delete',
                                                            theme_name=test_theme_name))
    assert response.status_int == 302
    response = webtest_admin_testapp.get(request.route_path('backend_theme_config_list'))
