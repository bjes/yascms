def test_login_logic(tp_yass_webtest):
    response = tp_yass_webtest.get('/backend/', expect_errors=True)
    assert response.status_int == 403

    response = tp_yass_webtest.get('/login')
    form = response.form
    form['account'] = 'wrong_account'
    form['password'] = 'wrong_password'
    response = form.submit()
    assert '登入失敗' in response.body.decode('utf8')

    response = tp_yass_webtest.get('/login')
    form = response.form
    form['account'] = 'admin'
    form['password'] = 'admin4tp_yass'
    form.submit()
    response = tp_yass_webtest.get('/backend/')
    assert '管理者' in response.body.decode('utf8')
