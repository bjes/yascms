from pyramid_wtforms import (Form,
                             StringField,
                             TextAreaField,
                             BooleanField,
                             SelectField,
                             HiddenField,
                             SubmitField,
                             FieldList,
                             FormField)
from pyramid_wtforms.validators import InputRequired, Length, ValidationError

from tp_yass.enum import ThemeConfigCustomType
from .fields import MultiCheckboxField

class ThemeConfigCustomForm(Form):
    """可讓使用者自訂的欄位"""

    name = StringField('變數名稱*', [InputRequired('此欄位必填'), Length(max=50, message='最長只接受 50 個字元')])

    type = SelectField('類型', [InputRequired('此欄位必選')],
                       choices=[(str(ThemeConfigCustomType.STRING.value), '字串'),
                                (str(ThemeConfigCustomType.BOOLEAN.value), '布林值'),
                                (str(ThemeConfigCustomType.INTEGER.value), '整數')],
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


class ThemeConfigBannerVisibleForm(Form):
    """用來處理是否啟用啟用單一橫幅"""

    # 這個欄位只是用來比對哪個橫幅是否有啟用，在前端不會顯示，其值的修改也不會有作用
    name = HiddenField('橫幅檔名')

    is_visible = BooleanField('是否啟用')


class ThemeConfigBannersEditForm(Form):
    """用來處理橫幅顯示與否的表單列表"""

    banners = FieldList(FormField(ThemeConfigBannerVisibleForm))

    submit = SubmitField('儲存顯示設定')

    def validate_banners(form, field):
        all_disabled = True
        for each_element in field.entries:
            if each_element.data['is_visible'] == True:
                all_disabled = False
        if all_disabled:
            raise ValidationError('至少要選一個橫幅')
