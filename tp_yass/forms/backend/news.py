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
                                        FileSize)


class NewsForm(Form):
    """最新消息的建立表單"""

    title = StringField('標題*', [InputRequired('此欄位必填'), Length(max=50, message='最長只接受 50 個字元')])

    content = TextAreaField('內容')

    # TODO: 要讓系統可以設定上傳的檔案大小限制，目前寫死必須小於 200 MB
    attachments = MultipleFilesField('附件', [FileSize(max=200, base='mb')])

    is_pinned = BooleanField('是否置頂')

    pinned_start_date = DateField('置頂開始時間', format='%Y-%m-%d %H:%M')

    pinned_end_date = DateField('置頂結束時間', format='%Y-%m-%d %H:%M')

    visible_start_date = DateTimeField('顯示開始時間（未指定則代表馬上顯示）')

    visible_end_date = DateTimeField('顯示結束時間（未指定則代表永遠顯示）')

    tags = StringField('標籤（以逗號分隔）')

    category_id = SelectField('分類群組', coerce=int)

    class Meta:
        locales = ['zh_TW', 'tw']


class NewsEditForm(NewsForm):
    """最新消息的編輯表單"""

    # 用來顯示已上傳的附件檔案列表，讓使用者可自由勾選是否刪除或保留
    uploaded_attachments = MultipleCheckboxField('已上傳的附件', coerce=int)

    class Meta:
        locales = ['zh_TW', 'tw']
