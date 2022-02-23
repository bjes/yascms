from datetime import datetime

from pyramid_wtforms import (Form,
                             StringField,
                             TextAreaField,
                             BooleanField,
                             DateTimeField,
                             SelectField,
                             MultipleFilesField,
                             MultipleCheckboxField)
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

    pinned_start_datetime = DateTimeField('置頂開始時間', format='%Y-%m-%d %H:%M:%S')

    pinned_end_datetime = DateTimeField('置頂結束時間', format='%Y-%m-%d %H:%M:%S')

    def check_visible_start_datetime(form, field):
        """檢查 visible_start_datetime 欄位

        其值必須是 None 或是 datetime.datetime 實體，且值要小於等於 visible_end_datetime
        """
        if field.data:
            if not isinstance(field.data, datetime):
                raise ValidationError('顯示開始時間必須是時間格式')
            if form.visible_end_datetime.data:
                if not isinstance(form.visible_end_datetime.data, datetime):
                    raise ValidationError('顯示結束時間必須是時間格式')
                if field.data > form.visible_end_datetime.data:
                    raise ValidationError('顯示開始時間必須早於或等於顯示結束時間')

    visible_start_datetime = DateTimeField('顯示開始時間（未指定則代表馬上顯示）',
                                           [check_visible_start_datetime, Optional()],
                                           format='%Y-%m-%d %H:%M:%S')

    def check_visible_end_datetime(form, field):
        """檢查 visible_end_datetime 欄位

        其值必須是 None 或是 datetime.datetime 實體，且值要大於等於 visible_end_datetime
        """
        if field.data:
            if not isinstance(field.data, datetime):
                raise ValidationError('顯示結束時間必須是時間格式')
            if form.visible_start_datetime.data:
                if not isinstance(form.visible_start_datetime.data, datetime):
                    raise ValidationError('顯示開始時間必須是時間格式')
                if field.data < form.visible_end_datetime.data:
                    raise ValidationError('顯示結束時間必須晚於或等於顯示開始時間')

    visible_end_datetime = DateTimeField('顯示結束時間（未指定則代表永遠顯示）',
                                         [check_visible_end_datetime, Optional()],
                                         format='%Y-%m-%d %H:%M:%S')

    tags = StringField('標籤（以逗號分隔）')

    group_id = SelectField('張貼群組', coerce=int)

    category_id = SelectField('分類群組', coerce=int)

    def validate_is_pinned(form, field):
        """若勾選了置頂，那麼置頂起訖日期都要設定"""
        if field.data is True:
            if not (isinstance(form.pinned_start_datetime.data, datetime)
                    and isinstance(form.pinned_end_datetime.data, datetime)):
                raise ValidationError('置頂起訖時間都需要指定')
            if form.pinned_end_datetime.data < form.pinned_start_datetime.data:
                raise ValidationError('置頂結束時間需晚於置頂開始日期')

    class Meta:
        locales = ['zh_TW', 'tw']


class NewsEditForm(NewsForm):
    """最新消息的編輯表單"""

    # 用來顯示已上傳的附件檔案列表，讓使用者可自由勾選是否刪除或保留
    uploaded_attachments = MultipleCheckboxField('已上傳的附件', coerce=int)

    class Meta:
        locales = ['zh_TW', 'tw']


class NewsCategoryForm(Form):
    """最新消息分類表單"""

    name = StringField('名稱*', [InputRequired('名稱必填')])

    # TODO: 要動態產生，目前先寫死 20 組
    order = SelectField('排序*', [InputRequired('排序必填')],
                        choices=[(i, str(i)) for i in range(21)],
                        coerce=int)

    class Meta:
        locales = ['zh_TW', 'tw']
