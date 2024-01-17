from pyramid.testing import DummyRequest
from webtest.forms import Radio

from yascms.enum import NavbarType


def test_navbar_list_view_should_return_navbar_list(webtest_admin_testapp):
    request = DummyRequest()
    response = webtest_admin_testapp.get(request.route_path('backend_navbar_list'))
    assert response.status_int == 200
    assert '導覽列列表' in response.body.decode('utf8')


def test_navbar_create_get_view_should_return_navbar_form(webtest_admin_testapp):
    request = DummyRequest()
    response = webtest_admin_testapp.get(request.route_path('backend_navbar_create'))
    assert response.status_int == 200
    assert '建立導覽列' in response.body.decode('utf8')


def fill_form(form, name, ancestor_id):
    form['name'] = name
    # ancestor_id 是前端動態產生的 field ，所以這邊用手動的方式加進去 webtest
    field = Radio(form, 'input', 'ancestor_id', 0, None, 'ancestor_id')
    form.fields['ancestor_id'] = [field]
    form.field_order.append(('ancestor_id', field))
    form['ancestor_id'].force_value(ancestor_id)
    return form


def test_navbar_create_post_view_should_create_navbar(webtest_admin_testapp):
    request = DummyRequest()
    ancestor_id = 1  # 上層指定為根導覽列
    form_name_field = 'foo_navbar'
    form_aria_name_field = 'foo_aria_name'

    # 正常建立 tree node
    response = webtest_admin_testapp.get(request.route_path('backend_navbar_create'))
    form = fill_form(response.form, form_name_field, ancestor_id)
    form['type'] = NavbarType.TREE_NODE.value
    form['aria_name'] = form_aria_name_field
    response = form.submit()
    assert response.status_int == 302
    response = webtest_admin_testapp.get(request.route_path('backend_navbar_list'))
    assert form_name_field in response.body.decode('utf8')

    # tree node 必須要有 aria_name
    response = webtest_admin_testapp.get(request.route_path('backend_navbar_create'))
    form = fill_form(response.form, form_name_field, ancestor_id)
    form['type'] = NavbarType.TREE_NODE.value
    response = form.submit()
    assert response.status_int == 200
    assert '建立失敗' in response.body.decode('utf8')

