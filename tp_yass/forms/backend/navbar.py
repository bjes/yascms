from pyramid_wtforms import (Form,
                             StringField,
                             SelectField,
                             IntegerField,
                             BooleanField)
from pyramid_wtforms.validators import InputRequired, Length, ValidationError


class NavbarForm(Form):
    """新增 navbar 的表單"""

    name = StringField('名稱', [InputRequired('名稱欄位為必填'), Length(min=1, max=50)])

    type = SelectField('導覽列類型',
                       [InputRequired('導覽列類型欄位必填')],
                       choices=[(1, '導覽列選單（可新增子選單）'),
                                (2, '導覽列連結（無法新增子選單）'),
                                (3, '分隔線')],
                       coerce=int)

    leaf_type = SelectField('導覽列連結類型',
                            [InputRequired('導覽列連結類型必填')],
                            choices=[(1, '連結單一頁面'),
                                     (2, '手動輸入網址')],
                            coerce=int)

    url = StringField('連結網址', [Length(max=500)])

    page_id = StringField('連結單一頁面')

    icon = StringField('圖示名稱', [Length(max=50)])

    is_external = BooleanField('連結另開視窗')

    is_visible = BooleanField('是否顯示', default='checked')

    # TODO: 要動態產生，目前先寫死 20 組
    order = SelectField('排序',
                        [InputRequired('排序必填')],
                        choices=[(i, str(i)) for i in range(21)],
                        coerce=int)

    ancestor_id = IntegerField('上層選單', [InputRequired('上層選單欄位必填')])

    class Meta:
        locales = ['zh_TW', 'tw']
