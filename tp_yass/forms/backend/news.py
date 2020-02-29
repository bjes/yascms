from datetime import datetime

from pyramid_wtforms import (Form,
                             StringField,
                             TextAreaField,
                             MultipleCheckboxField,
                             BooleanField,
                             DateTimeField,
                             DateField,
                             SelectField,
                             MultipleFilesField)
from pyramid_wtforms.validators import (InputRequired,
                                        Length,
                                        FileSize,
                                        Optional,
                                        ValidationError)


class NewsForm(Form):
    """最新消息的建立表單"""

    title = StringField('標題*', [InputRequired('標題欄位必填'), Length(max=50, message='最長只接受 50 個字元')])

    content = TextAreaField('內容*', [InputRequired('內容欄位必填')])

    # TODO: 要讓系統可以設定上傳的檔案大小限制，目前寫死必須小於 200 MB
    attachments = MultipleFilesField('附件', [FileSize(max=200, base='mb')])

    is_pinned = BooleanField('是否置頂')

    pinned_start_date = DateField('置頂開始日期', format='%Y-%m-%d', validators=[Optional()])

    pinned_end_date = DateField('置頂結束日期', format='%Y-%m-%d', validators=[Optional()])

    visible_start_date = DateTimeField('顯示開始時間（未指定則代表馬上顯示）',
                                       format='%Y-%m-%d %H:%M',
                                       validators=[Optional()])

    visible_end_date = DateTimeField('顯示結束時間（未指定則代表永遠顯示）',
                                     format='%Y-%m-%d %H:%M',
                                     validators=[Optional()])

    tags = StringField('標籤（以逗號分隔）')

    category_id = SelectField('分類群組', coerce=int)

    def validate_is_pinned(form, field):
        """若勾選了置頂，那麼置頂起訖日期都要設定"""
        if field.data is True:
            if not (isinstance(form.pinned_start_date.data, datetime)
                    and isinstance(form.pinned_end_date.data, datetime)):
                raise ValidationError('置頂起訖日期都需要指定')

    class Meta:
        locales = ['zh_TW', 'tw']


class NewsEditForm(NewsForm):
    """最新消息的編輯表單"""

    # 用來顯示已上傳的附件檔案列表，讓使用者可自由勾選是否刪除或保留
    uploaded_attachments = MultipleCheckboxField('已上傳的附件', coerce=int)

    class Meta:
        locales = ['zh_TW', 'tw']
