from pyramid_wtforms import (Form,
                             IntegerField,
                             StringField,
                             SelectField,
                             PasswordField,
                             RadioField,
                             FormField,
                             FieldList,
                             MultipleCheckboxField)
from pyramid_wtforms.validators import (InputRequired,
                                        Length,
                                        Email,
                                        EqualTo,
                                        Optional,
                                        ValidationError)

from yascms.enum import GroupType


class UserEssentialFieldsForm(Form):
    """使用者基礎欄位的表單，一般使用者可以自訂的欄位都放在這"""

    first_name = StringField('名*', [InputRequired('名為必填'), Length(max=20)])

    last_name = StringField('姓*', [InputRequired('姓為必填'), Length(max=20)])

    # 密碼不一定要設定
    password = PasswordField('密碼 (留空代表不更動)', [Length(max=50)])

    password_confirm = PasswordField('再次輸入密碼 (留空代表不更動)', [Length(max=50), EqualTo('password', message='兩次密碼輸入需相符')])


class UserSelfEditForm(UserEssentialFieldsForm):
    """使用者可以自己更改設定的表單"""

    old_password = PasswordField('舊密碼 (留空代表不更動)', [Length(max=50)])


class EmailForm(Form):
    """處理關聯至帳號與群組的 Email"""

    address = StringField('電子郵件位址*', [InputRequired('電子郵件為必填'), Length(max=100), Email('需為合法的電子郵件位址')])


class AdminUserCreateForm(UserEssentialFieldsForm):
    """管理者建立使用者的表單"""

    email = FieldList(FormField(EmailForm), min_entries=1)

    # 用來在前端讓使用者勾選，多個 email 的列表中，哪一個是 primary email
    primary_email = RadioField('主要郵件位址', [InputRequired('主要郵件位址必填'), Email('需為合法的電子郵件位址')])

    def validate_primary_email(form, field):
        email_list = [each_email['address'] for each_email in form.email.data]
        if field.data not in email_list:
            raise ValidationError('不合法的 primary email')

    account = StringField('帳號*', [InputRequired('帳號為必填'), Length(max=50)])

    # 建立使用者時強制要設定密碼
    password = PasswordField('密碼*', [InputRequired('密碼為必填'), Length(max=50)])

    password_confirm = PasswordField('再次輸入密碼*', [InputRequired('需再次輸入密碼'),
                                                     Length(max=50),
                                                     EqualTo('password', message='兩次密碼輸入需相符')])

    # 只是用來驗證，前端會靠 jquery bonsai 產生巢狀多選選單，不會依靠這個 field 產生
    group_ids = MultipleCheckboxField('群組*', [InputRequired('至少要選一個群組')], coerce=int)


class AdminUserEditForm(AdminUserCreateForm):
    """管理者編輯使用者的表單，密碼欄位因為允許使用者不用更改，所以移除 validator"""

    password = PasswordField('密碼*', [Length(max=50)])

    password_confirm = PasswordField('再次輸入密碼*', [Length(max=50),
                                                     EqualTo('password', message='兩次密碼輸入需相符')])


class GroupCreateForm(Form):
    """建立使用者群組的表單"""

    name = StringField('群組名稱*', [InputRequired('群組名稱為必填'), Length(max=100)])

    type = SelectField('類別*',
                       [InputRequired('群組類別為必填')],
                       choices=[(GroupType.STAFF.value, '行政群組'),
                                (GroupType.NORMAL.value, '一般群組'),
                                (GroupType.ADMIN.value, '管理群組')],
                       coerce=int)

    email = FieldList(FormField(EmailForm))

    def check_primary_email(form, field):
        email_list = [each_email['address'] for each_email in form.email.data]
        if email_list and (field.data not in email_list):
            raise ValidationError('不合法的 primary email')

    # 用來在前端讓使用者勾選，多個 email 的列表中，哪一個是 primary email。相關的列表會在 view
    # 那邊動態產生與處理，這邊只是定義有這個欄位，驗證等都是在 view 那邊處理
    # 群組沒有強制一定要輸入 email，所以這邊是選填，驗證的部份在 view 那邊處理
    # 不在這邊自己刻驗證的原因是覺得，直接在 view 那邊比對是否符合有填入的 email 即可
    # 驗證的部份經過實測，必須先放自訂的驗證，再放 Optional() 才可以讓這個表單欄位可填可不填，
    # 並在有值的時候，用我們自訂的驗證邏輯去驗證
    primary_email = RadioField('主要郵件位址', [check_primary_email, Optional()], choices=[])

    # TODO: 要動態產生，目前先寫死 20 組
    order = SelectField('排序*', [InputRequired('排序必填')],
                        choices=[(i, str(i)) for i in range(21)],
                        coerce=int)

    ancestor_id = IntegerField('上層群組')
