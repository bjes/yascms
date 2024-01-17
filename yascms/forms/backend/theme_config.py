import json
import logging

from pyramid_wtforms import (Form,
                             StringField,
                             TextAreaField,
                             BooleanField,
                             SelectField,
                             HiddenField,
                             SubmitField,
                             FileField,
                             MultipleFilesField,
                             FieldList,
                             FormField)
from pyramid_wtforms.validators import (InputRequired,
                                        Length,
                                        FileRequired,
                                        FileSize,
                                        FileAllowed,
                                        ValidationError)

from yascms.dal import DAL
from yascms.enum import ThemeConfigCustomType, HomepageItemType, HomepageItemParamsSubType


logger = logging.getLogger(__name__)


class ThemeConfigCustomForm(Form):
    """可讓使用者自訂的欄位"""

    name = StringField('變數名稱*', [InputRequired('此欄位必填'), Length(max=50, message='最長只接受 50 個字元')])

    type = SelectField('類型', [InputRequired('此欄位必選')],
                       choices=[(str(ThemeConfigCustomType.STRING.value), '字串'),
                                (str(ThemeConfigCustomType.BOOLEAN.value), '布林值'),
                                (str(ThemeConfigCustomType.INTEGER.value), '整數')],
                       coerce=int)

    value = StringField('變數內容')

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

    def validate_banners(form, field):
        all_disabled = True
        for each_element in field.entries:
            if each_element.data['is_visible'] == True:
                all_disabled = False
        if all_disabled:
            raise ValidationError('至少要選一個橫幅')


class ThemeConfigBannersUploadForm(Form):
    """上傳橫幅的表單"""

    banners = MultipleFilesField('上傳橫幅', [FileRequired('請上傳橫幅檔案'),
                                             FileAllowed(['png', 'jpg', 'jpeg']),
                                             FileSize(max=20, base='mb', message='檔案不能大於 20 MB')])


class ThemeConfigUploadForm(Form):
    """上傳樣板的表單"""

    theme = FileField('上傳樣板', [FileRequired('請上傳樣板'),
                                  FileAllowed(['zip']),
                                  FileSize(max=50, base='mb', message='檔案不能大於 50 MB')])

    is_overwrite = BooleanField('是否覆寫現有樣板')


class ThemeConfigHomepageItemsOrderEditForm(Form):
    """設定首頁元件順序的表單"""

    config = TextAreaField('設定值', [InputRequired('此欄位必填')])

    def validate_config(form, field):
        """
        TODO: 重構成物件導向，使用物件呈現設定值而非直接處理資料結構
        """
        valid_keys = ['name', 'type', 'params']
        try:
            for each_item in json.loads(field.data):
                for key in valid_keys:
                    if key not in valid_keys:
                        raise ValidationError(f'設定值含有不合法的鍵值: {key}')
                item_type = HomepageItemType(each_item['type'])
                if item_type == HomepageItemType.NEWS.value:
                    if not (each_item['params']['sub_type'] == HomepageItemParamsSubType.UNSPECIFIED.value or
                            each_item['params']['sub_type'] in [each_news_category.id for each_news_category
                                                                in DAL.get_news_category_list()]):
                        raise ValidationError(f'找不到最新消息分類 ID {item_type}')
                    news_quantity = each_item['params'].get('quantity', None)
                    # TODO: 最新消息的顯示數量上限值應該要拉出來
                    if not (isinstance(news_quantity, int) and news_quantity <= 100):
                        raise ValidationError('最新消息顯示數量設定值不合法，需小於等於 100')
                elif item_type == HomepageItemType.LINKS.value:
                    if not (each_item['params']['sub_type'] == HomepageItemParamsSubType.UNSPECIFIED.value or
                            each_item['params']['sub_type'] in [each_link_category.id for each_link_category
                                                                in DAL.get_link_category_list()]):
                        raise ValidationError(f'找不到好站連結分類 ID {item_type}')
                elif item_type == HomepageItemType.PAGE.value:
                    page_id = each_item['params'].get('id', None)
                    if not (isinstance(page_id, int) and DAL.get_page(page_id)):
                        raise ValidationError('指涉的單一頁面不存在')
        except (ValueError, KeyError) as err:
            logger.error(err)
            raise ValidationError(f'類別或子類別含有不合法的設定值：{err}')
