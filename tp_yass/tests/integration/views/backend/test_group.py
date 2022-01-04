from pyramid.testing import DummyRequest
from webtest.forms import Radio, Text


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
    ancestor_group_id = '3'  # 上層單位設定成測試學校

    # 測試可以建立本來不存在的群組
    response = webtest_admin_testapp.get(request.route_path('backend_group_create'))
    assert group_name not in response.body.decode('utf8')
    form = fill_form(response.form, group_name, ancestor_group_id)
    response = form.submit()
    assert response.status_int == 302
    response = webtest_admin_testapp.get(request.route_path('backend_group_list'))
    assert group_name in response.body.decode('utf8')

    # 可以建立同名的群組
    response = webtest_admin_testapp.get(request.route_path('backend_group_create'))
    form = fill_form(response.form, group_name, ancestor_group_id)
    response = form.submit()
    assert response.status_int == 302
    response = webtest_admin_testapp.get(request.route_path('backend_group_list'))
    assert response.body.decode('utf8').count(group_name) == 3  # 兩筆群組、加上 flash 成功訊息裡面也會顯示

    # 一個群組可以建立多組 email
    response = webtest_admin_testapp.get(request.route_path('backend_group_create'))
    form = fill_form(response.form, group_name, ancestor_group_id)
    # email 相關的欄位都是前端動態產生，所以這邊要處理
    pri_email = 'pri_group@example.com'
    sec_email = 'sec_group@example.com'
    field = Radio(form, 'input', 'primary_email', 0, None, 'primary_email')
    form.fields['primary_email'] = [field]
    form.field_order.append(('primary_email', field))
    form['primary_email'].force_value(pri_email)
    field_name = 'email-0-address'
    field = Text(form, 'input', field_name, 0, None, field_name)
    form.fields[field_name] = [field]
    form.field_order.append((field_name, field))
    form[field_name].force_value(pri_email)
    field_name = 'email-1-address'
    field = Text(form, 'input', field_name, 0, None, field_name)
    form.fields[field_name] = [field]
    form.field_order.append((field_name, field))
    form[field_name].force_value(sec_email)
    response = form.submit()
    assert response.status_int == 302
    response = webtest_admin_testapp.get(request.route_path('backend_group_list'))
    html_content = response.body.decode('utf8')
    assert pri_email in html_content
    assert sec_email in html_content

    # 群組若建立的 email 中已存在且不是關聯到此群組，會回報錯誤
    response = webtest_admin_testapp.get(request.route_path('backend_group_create'))
    form = fill_form(response.form, group_name, ancestor_group_id)
    # email 相關的欄位都是前端動態產生，所以這邊要處理
    existed_email = 'webmaster@example.org',
    field = Radio(form, 'input', 'primary_email', 0, None, 'primary_email')
    form.fields['primary_email'] = [field]
    form.field_order.append(('primary_email', field))
    form['primary_email'].force_value(existed_email)
    field_name = 'email-0-address'
    field = Text(form, 'input', field_name, 0, None, field_name)
    form.fields[field_name] = [field]
    form.field_order.append((field_name, field))
    form[field_name].force_value(existed_email)
    response = form.submit()
    assert response.status_int == 200


def test_group_edit_view_should_change_group_attributes(webtest_admin_testapp):
    request = DummyRequest()
    ancestor_group_id = 1

    # 取得測試國小的群組
    response = webtest_admin_testapp.get(request.route_path('backend_group_edit', group_id=3))
    form = response.form
    # email 相關的欄位都是前端動態產生，所以這邊要處理
    school_email = 'school@example.org'
    field = Radio(form, 'input', 'primary_email', 0, None, 'primary_email')
    form.fields['primary_email'] = [field]
    form.field_order.append(('primary_email', field))
    form['primary_email'].force_value(school_email)
    field_name = 'email-0-address'
    field = Text(form, 'input', field_name, 0, None, field_name)
    form.fields[field_name] = [field]
    form.field_order.append((field_name, field))
    form[field_name].force_value(school_email)
    # ancestor_id 是前端動態產生的 field ，所以這邊用手動的方式加進去 webtest
    field = Radio(form, 'input', 'ancestor_id', 0, None, 'ancestor_id')
    form.fields['ancestor_id'] = [field]
    form.field_order.append(('ancestor_id', field))
    form['ancestor_id'].force_value(ancestor_group_id)
    form.submit()
    response = webtest_admin_testapp.get(request.route_path('backend_group_list'))
    assert school_email in response.body.decode('utf8')

