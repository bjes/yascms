from pyramid_wtforms import (Form,
                             IntegerField,
                             StringField,
                             SelectField,
                             PasswordField)
from pyramid_wtforms.validators import (InputRequired,
                                        Length,
                                        Email,
                                        EqualTo)

from .fields import MultiCheckboxField


class UserForm(Form):
    """建立使用者的表單"""

    first_name = StringField('名*', [InputRequired('名為必填'), Length(max=20)])

    last_name = StringField('姓*', [InputRequired('姓為必填'), Length(max=20)])

    email = StringField('電子郵件*', [InputRequired('電子郵件為必填'), Length(max=50), Email('需為合法的電子郵件位址')])

    account = StringField('帳號*', [InputRequired('帳號為必填'), Length(max=50)])

    password = PasswordField('密碼*', [InputRequired('密碼為必填'), Length(max=50)])

    password_confirm = PasswordField('再次輸入密碼*', [InputRequired('需再次輸入密碼'),
                                                      Length(max=50),
                                                      EqualTo('password', message='兩次密碼輸入需相符')])

    # 只是用來驗證，前端會靠 jquery bonsai 產生巢狀多選選單，不會依靠這個 field 產生
    group_ids = MultiCheckboxField('群組*', [InputRequired('至少要選一個群組')], coerce=int)


class UserEditForm(UserForm):
    """編輯使用者的表單，密碼欄位因為允許不更改，所以移除 validator"""

    password = PasswordField('密碼*', [Length(max=50)])

    password_confirm = PasswordField('再次輸入密碼*', [Length(max=50),
                                                     EqualTo('password', message='兩次密碼輸入需相符')])


class UserGroupForm(Form):
    """使用者群組的表單"""

    name = StringField('群組名稱*', [InputRequired('群組名稱為必填'), Length(max=100)])

    type = SelectField('類別*',
                       [InputRequired('群組類別為必填')],
                       choices=[(1, '行政群組'), (2, '普通群組'), (0, '管理者')],
                       coerce=int)

    # TODO: 要動態產生，目前先寫死 20 組
    order = SelectField('排序*', [InputRequired('排序必填')],
                        choices=[(i, str(i)) for i in range(21)],
                        coerce=int)

    ancestor_id = IntegerField('上層群組')
