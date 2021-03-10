from pyramid.testing import DummyRequest

def add_link_category(response, name):
    """新增指定的連結分類
    
    Args:
        response: webtest.response.TestResponse 實體
        name: 連結分類名稱

    Returns:
        webtest.response.TestResponse 實體
    """
    form = response.form
    form['name'] = name
    return form.submit()


def test_link_category_create_view(webtest_admin_testapp):
    request = DummyRequest()

    # 取得表單
    response = webtest_admin_testapp.get(request.route_path('backend_link_category_create'))
    assert response.status_int == 200

    # 填表單送出，只填 name 欄位
    link_category_name = 'test連結分類'
    response = add_link_category(response, link_category_name)
    assert response.status_int == 302


def test_link_category_list_view(webtest_admin_testapp):
    request = DummyRequest()

    # 先建立測試連結分類
    response = webtest_admin_testapp.get(request.route_path('backend_link_category_create'))
    link_category_name = 'test連結分類'
    add_link_category(response, link_category_name)
    
    # 驗證網頁有沒有上面新增的分類
    response = webtest_admin_testapp.get(request.route_path('backend_link_category_list'))
    assert link_category_name in response.body.decode('utf8')
