from pyramid.testing import DummyRequest
from webtest.forms import Radio


def fill_form(form, name, ancestor_id):
    form['name'] = name
    # ancestor_id 是前端動態產生的 field ，所以這邊用手動的方式加進去 webtest
    field = Radio(form, 'input', 'ancestor_id', 0, None, 'ancestor_id')
    form.fields['ancestor_id'] = [field]
    form.field_order.append(('ancestor_id', field))
    form['ancestor_id'].force_value(ancestor_id)
    return form


def test_group_create_view_and_list_view_should_create_and_show_group(webtest_admin_testapp):
    request = DummyRequest()
    group_name = '測試處室'
    ancestor_group_id = '2' # 上層單位設定成測試學校

    # 測試可以建立本來不存在的群組
    response = webtest_admin_testapp.get(request.route_path('backend_group_create'))
    assert group_name not in response.body.decode('utf8')
    form = fill_form(response.form, group_name, ancestor_group_id)
    form.submit()
    response = webtest_admin_testapp.get(request.route_path('backend_group_create'))
    assert group_name in response.body.decode('utf8')

    # 可以建立同名的群組
    response = webtest_admin_testapp.get(request.route_path('backend_group_create'))
    form = fill_form(response.form, group_name, ancestor_group_id)
    response = form.submit()
    assert response.status_int == 302
    response = webtest_admin_testapp.get(request.route_path('backend_group_create'))
    assert response.body.decode('utf8').count(group_name) == 2
