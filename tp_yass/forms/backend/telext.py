from pyramid_wtforms import (Form,
                             StringField,
                             BooleanField,
                             SelectField)
from pyramid_wtforms.validators import (InputRequired,
                                        Length,
                                        ValidationError)


class TelExtForm(Form):
    """分機表的建立表單"""

    title = StringField('標題*', [InputRequired('標題欄位必填'), Length(max=50, message='最長只接受 50 個字元')])

    ext = StringField('分機*', [InputRequired('分機欄位必填'), Length(max=50, message='最長只接受 50 個字元')])

    is_pinned = BooleanField('是否於首頁顯示')

    # TODO: 要動態產生，目前先寫死 20 組
    order = SelectField('排序', [InputRequired('排序必填')],
                        choices=[(i, str(i)) for i in range(21)],
                        coerce=int)

    def validate_ext(form, field):
        """分機欄位必須是數值的字串"""
        if not field.data.isdigit():
            raise ValidationError('分機需為數字組成')

    class Meta:
        locales = ['zh_TW', 'tw']
