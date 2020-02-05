from pyramid_wtforms import (Form,
                             StringField,
                             PasswordField)
from pyramid_wtforms.validators import InputRequired, Length


class LoginForm(Form):
    account = StringField('帳號', [InputRequired('帳號為必填'), Length(max=50, message='帳號長度需低於 50')])
    password = PasswordField('密碼', [InputRequired('密碼為必填'), Length(max=130, message='密碼長度需低於 130')])
