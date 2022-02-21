from pyramid.testing import DummyRequest
from webtest.forms import Radio, Text, Checkbox


def fill_form(form, account, primary_email='primary@example.org', secondary_email='secondary@example.org'):
    form['first_name'] = 'first_name'
    form['last_name'] = 'last_name'

    field = Radio(form, 'input', 'primary_email', 0, None, 'primary_email')
    form.fields['primary_email'] = [field]
    form.field_order.append(('primary_email', field))
    form['primary_email'].force_value(primary_email)

    field = Text(form, 'input', 'email-0-address', 0, None, 'email-0-address')
    form.fields['email-0-address'] = [field]
    form.field_order.append(('email-0-address', field))
    form['email-0-address'].force_value(primary_email)

    field = Text(form, 'input', 'email-1-address', 0, None, 'email-1-address')
    form.fields['email-1-address'] = [field]
    form.field_order.append(('email-1-address', field))
    form['email-1-address'].force_value(secondary_email)

    field = Checkbox(form, 'input', 'group_ids', 0, None, 'group_ids')
    form.fields['group_ids'] = [field]
    form.field_order.append(('group_ids', field))
    group_ids = ['8', '5']  # 系管師、自然科任
    form['group_ids'].value = group_ids
    form['group_ids'].force_value(group_ids)

    form['account'] = account
    form['password'] = 'bar'
    form['password_confirm'] = 'bar'
    return form


def test_user_create_view_and_list_view_should_create_and_show_user(webtest_admin_testapp):
    request = DummyRequest()
    account_name = 'foo'

    # 測試可以建立本來不存在的使用者
    response = webtest_admin_testapp.get(request.route_path('backend_user_create'))
    assert account_name not in response.body.decode('utf8')
    form = fill_form(response.form, account_name)
    response = form.submit()
    assert response.status_int == 302
    response = webtest_admin_testapp.get(request.route_path('backend_user_list'))
    assert account_name in response.body.decode('utf8')

    # 不可以建立同名的使用者
    response = webtest_admin_testapp.get(request.route_path('backend_user_create'))
    form = fill_form(response.form, account_name, primary_email='oops@example.org', secondary_email='oops2@example.org')
    response = form.submit()
    assert response.status_int == 200
    response = webtest_admin_testapp.get(request.route_path('backend_user_list'))
    assert response.body.decode('utf8').count(account_name) == 1

    # 若建立的 email 中已存在且不是關聯到此使用者，會回報錯誤
    new_account = 'bar'
    response = webtest_admin_testapp.get(request.route_path('backend_user_create'))
    # webmaster@example.org 是已存在的測試 email，所以這個新建使用者帳號的 email 會跟已存在的重複
    form = fill_form(response.form, new_account,
                     primary_email='webmaster@example.org', secondary_email='yet_another@example.org')
    response = form.submit()
    assert response.status_int == 200


def test_user_edit_view_should_change_user_attributes(webtest_admin_testapp):
    request = DummyRequest()
    new_email = 'user999@example.com'

    # 取得測試帳號陳小明
    response = webtest_admin_testapp.get(request.route_path('backend_user_edit', user_id=2))
    form = fill_form(response.form, account='user1',
                     primary_email=new_email, secondary_email='user998@example.com')
    form.submit()
    response = webtest_admin_testapp.get(request.route_path('backend_user_list'))
    assert new_email in response.body.decode('utf8')


def test_user_self_edit_view_should_change_user_attributes(webtest_testapp):
    request = DummyRequest()
    account = 'user1'
    old_first_name = '小明'
    new_first_name = '小王'
    old_password = 'user1'
    new_password = 'bar'

    response = webtest_testapp.get(request.route_path('login'))
    form = response.form
    form['account'] = account
    form['password'] = old_password
    form.submit()

    response = webtest_testapp.get(request.route_path('backend_user_self_edit'))
    assert new_first_name not in response.body.decode('utf8')
    form = response.form
    form['first_name'] = new_first_name
    form['old_password'] = old_password
    form['password'] = new_password
    form['password_confirm'] = new_password
    form.submit()

    response = webtest_testapp.get(request.route_path('backend_user_self_edit'))
    assert new_first_name in response.body.decode('utf8')

    response = webtest_testapp.get(request.route_path('logout'))
    response = webtest_testapp.get(request.route_path('login'))
    form = response.form
    form['account'] = account
    form['password'] = new_password
    response = form.submit()

    assert response.status_int == 302
    response = webtest_testapp.get(request.route_path('backend_user_self_edit'))
    assert new_first_name in response.body.decode('utf8')

