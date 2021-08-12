from pyramid.testing import DummyRequest


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
