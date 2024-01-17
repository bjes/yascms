from pyramid_wtforms import (Form,
                             StringField,
                             SelectField,
                             IntegerField,
                             HiddenField,
                             BooleanField)
from pyramid_wtforms.widgets import HiddenInput
from pyramid_wtforms.validators import InputRequired, Length, ValidationError

from yascms.enum import NavbarType, NavbarLeafNodeType


class NavbarForm(Form):
    """新增 navbar 的表單"""

    name = StringField('名稱*', [InputRequired('名稱欄位為必填'), Length(min=1, max=50)])

    type = SelectField('導覽列類型*',
                       [InputRequired('導覽列類型欄位必填')],
                       choices=[(NavbarType.TREE_NODE.value, '導覽列選單（可新增子選單）'),
                                (NavbarType.LEAF_NODE.value, '導覽列連結（無法新增子選單）'),
                                (NavbarType.DROPDOWN_DIVIDER.value, '分隔線')],
                       coerce=int)

    aria_name = StringField('無障礙導覽列英文名稱*')

    def validate_aria_name(form, field):
        if field.data:
            if len(field.data) > 50:
                raise ValidationError('無障礙導覽列英文名稱長度不能超過 50 個字元')

    # 前端會處理顯示的部份，這邊只負責驗證，允許的值為 NavbarLeafNodeType.PAGE (代表連結單一頁面) 
    # 與 NavbarLeafNodeType.URL (代表自訂網址)。
    # 但要注意，如果是內建模組（像是最新消息等），我們只允許讓這些模組移動在導覽列的位置，此時這個值會忽略不處理
    leaf_type = HiddenField('導覽列連結類型')

    def validate_leaf_type(form, field):
        if field.data:
            if not (field.data.isdigit() and int(field.data) in (NavbarLeafNodeType.PAGE, NavbarLeafNodeType.URL)):
                raise ValidationError('此欄位合法值為 NavbarLeafNodeType.PAGE 或 NavbarLeafNodeType.URL')

    url = StringField('連結網址', [Length(max=500)])

    page_id = StringField('連結單一頁面')

    icon = StringField('圖示名稱', [Length(max=50)])

    is_href_blank = BooleanField('連結另開分頁')

    is_visible = BooleanField('是否顯示', default='checked')

    # TODO: 要動態產生，目前先寫死 20 組
    order = SelectField('排序',
                        [InputRequired('排序必填')],
                        choices=[(i, str(i)) for i in range(21)],
                        coerce=int)

    ancestor_id = IntegerField('上層導覽列')

    class Meta:
        locales = ['zh_TW', 'tw']


class NavbarEditForm(NavbarForm):
    """編輯導覽列的選單不需要讓使用者更改 type，這個欄位在編輯時不給改"""

    type = IntegerField('導覽列類型', [InputRequired('導覽列類型欄位必填')], widget=HiddenInput())
