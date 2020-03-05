from pyramid_wtforms import (Form,
                             IntegerField,
                             StringField,
                             SelectField,)
from pyramid_wtforms.validators import InputRequired, Length


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
