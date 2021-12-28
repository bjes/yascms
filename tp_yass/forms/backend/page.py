from pyramid_wtforms import (Form,
                             StringField,
                             TextAreaField,
                             MultipleFilesField,
                             MultipleCheckboxField)
from pyramid_wtforms.validators import (InputRequired,
                                        Length,
                                        FileSize)


class PageForm(Form):
    """單一網頁的建立表單"""

    title = StringField('標題*', [InputRequired('此欄位必填'), Length(max=100, message='最長只接受 100 個字元')])

    content = TextAreaField('內容')

    # 只是用來驗證，前端會靠 jquery bonsai 產生巢狀多選選單，不會依靠這個 field 產生
    group_ids = MultipleFilesField('管理群組*', [InputRequired('至少要選一個群組')], coerce=int)

    # TODO: 要讓系統可以設定上傳的檔案大小限制，目前寫死必須小於 200 MB
    attachments = MultipleFilesField('附件', [FileSize(max=200, base='mb')])

    tags = StringField('標籤（以逗號分隔）')

    class Meta:
        locales = ['zh_TW', 'tw']


class PageEditForm(PageForm):
    """單一網頁的編輯表單"""

    # 用來顯示已上傳的附件檔案列表，讓使用者可自由勾選是否刪除或保留
    uploaded_attachments = MultipleCheckboxField('已上傳的附件', coerce=int)

    class Meta:
        locales = ['zh_TW', 'tw']
