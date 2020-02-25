from pyramid_wtforms import (Form,
                             StringField,
                             TextAreaField,
                             MultipleCheckboxField,
                             MultipleFilesField)
from pyramid_wtforms.validators import (InputRequired,
                                        Length,
                                        FileSize)


class PageForm(Form):
    """單一網頁的建立表單"""

    title = StringField('標題*', [InputRequired('此欄位必填'), Length(max=100, message='最長只接受 50 個字元')])

    content = TextAreaField('內容')

    groups = StringField('群組*', [InputRequired('必須指定至少 1 個群組')])

    # TODO: 要讓系統可以設定上傳的檔案大小限制，目前寫死必須小於 200 MB
    attachments = MultipleFilesField('附件', [FileSize(max=200, base='mb')])

    tags = StringField('標籤')


class PageEditForm(PageForm):
    """單一網頁的編輯表單"""

    # 用來顯示已上傳的附件檔案列表，讓使用者可自由勾選是否刪除或保留
    uploaded_attachments = MultipleCheckboxField('已上傳的附件', coerce=int)
