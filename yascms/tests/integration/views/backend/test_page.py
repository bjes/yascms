from pyramid.testing import DummyRequest
from webtest.forms import Checkbox


def fill_form(form, title, content, group_ids):
    form['title'] = title
    form['content'] = content

    field = Checkbox(form, 'input', 'group_ids', 0, None, 'group_ids')
    form.fields['group_ids'] = [field]
    form.field_order.append(('group_ids', field))
    form['group_ids'].value = group_ids
    form['group_ids'].force_value(group_ids)

    return form


def test_page_list_should_list_all_pages(webtest_admin_testapp):
    request = DummyRequest()

    response = webtest_admin_testapp.get(request.route_path('backend_page_list'))
    assert response.status_int == 200
    assert '單一頁面列表' in response.body.decode('utf8')


def test_modify_page_should_change_the_page_content(webtest_admin_testapp):
    request = DummyRequest()
    test_group_ids = [3, 8]  # 測試國小、系管師 群組

    test_title = 'test title'
    test_content = 'test content'
    response = webtest_admin_testapp.get(request.route_path('backend_page_create'))
    form = fill_form(response.form, test_title, test_content, test_group_ids)
    response = form.submit()
    response_content = response.body.decode('utf8')
    assert response.status_int == 302
    response = webtest_admin_testapp.get(request.route_path('backend_page_list'))
    assert test_title in response.body.decode('utf8')

    test_page_id = 14  # 上面建立的測試單一頁面，其 id 為 14
    test_title = 'modified title'
    test_content = 'modified content'
    response = webtest_admin_testapp.get(request.route_path('backend_page_edit', page_id=test_page_id))
    form = fill_form(response.form, test_title, test_content, test_group_ids)
    response = form.submit()
    assert response.status_int == 302
    response = webtest_admin_testapp.get(request.route_path('backend_page_list'))
    assert test_title in response.body.decode('utf8')

    response = webtest_admin_testapp.get(request.route_path('backend_page_delete', page_id=test_page_id))
    assert response.status_int == 302
    response = webtest_admin_testapp.get(request.route_path('backend_page_list'))
    assert f'{test_title} 刪除成功' in response.body.decode('utf8')
