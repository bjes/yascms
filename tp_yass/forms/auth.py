from pyramid_wtforms import (Form,
                             StringField,
                             PasswordField)
from pyramid_wtforms.validators import InputRequired


class LoginForm(Form):
    account = StringField('帳號', [InputRequired('帳號為必填')])
    password = PasswordField('密碼', [InputRequired('密碼為必填')])
