from pyramid_wtforms import Form, StringField, BooleanField, TextAreaField
from pyramid_wtforms.validators import InputRequired, Length


class APITokenForm(Form):
    """api token 的建立表單"""

    name = StringField('名稱*', [InputRequired('名稱欄位必填'), Length(max=50, message='名稱最長為 50 個字元')])

    description = TextAreaField('說明')

    is_enabled = BooleanField('是否啟用', default='checked')

    class Meta:
        locales = ['zh_TW', 'tw']
