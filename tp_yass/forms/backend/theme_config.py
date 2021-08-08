from pyramid_wtforms import (Form,
                             StringField,
                             TextAreaField,
                             BooleanField,
                             SelectField,
                             FieldList,
                             FormField)
from pyramid_wtforms.validators import InputRequired, Length

from tp_yass.enum import ThemeConfigCustomType
from .fields import MultiCheckboxField

class ThemeConfigCustomForm(Form):
    """可讓使用者自訂的欄位"""

    name = StringField('變數名稱*', [InputRequired('此欄位必填'), Length(max=50, message='最長只接受 50 個字元')])

    type = SelectField('類型', [InputRequired('此欄位必選')],
                       choices=[(str(ThemeConfigCustomType.STRING.value), '字串'),
                                (str(ThemeConfigCustomType.BOOLEAN.value), '布林值'),
                                (str(ThemeConfigCustomType.INTEGER.value), '整數'),
                                (str(ThemeConfigCustomType.FLOAT.value), '浮點數')],
                       coerce=int)

    value = StringField('變數內容*', [InputRequired('此欄位必填'), ])

    description = StringField('變數說明', [Length(max=100, message='變數說明最長只接受 100 個字元')])


class ThemeConfigGeneralForm(Form):
    """編輯樣板設定的表單"""

    custom_css = TextAreaField('自訂 CSS')

    custom_css_visible = BooleanField('啟用自訂 CSS')

    custom_js = TextAreaField('自訂 JavaScript')

    custom_js_visible = BooleanField('啟用自訂 JavaScript')

    custom = FieldList(FormField(ThemeConfigCustomForm), label='自訂樣板變數')
