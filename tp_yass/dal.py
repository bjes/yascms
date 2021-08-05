"""資料庫存取抽象層

為了避免 views 相依 orm 操作，所以抽象資料存取層
"""
import json
import math
import logging
from datetime import datetime, date

from sqlalchemy import or_, func
from sqlalchemy.exc import IntegrityError
from pyramid_sqlalchemy import Session as DBSession

from tp_yass.models.account import UserModel, GroupModel
from tp_yass.models.news import NewsModel, NewsCategoryModel, NewsAttachmentModel
from tp_yass.models.navbar import NavbarModel
from tp_yass.models.config import ConfigModel
from tp_yass.models.page import PageModel, PageAttachmentModel
from tp_yass.models.tag import TagModel
from tp_yass.models.link import LinkModel, LinkCategoryModel
from tp_yass.models.telext import TelExtModel
from tp_yass.models.theme_config import ThemeConfigModel
from tp_yass.models.auth_log import AuthLogModel
from tp_yass.enum import GroupType, NavbarType


logger = logging.getLogger(__name__)


class DAL:

    @staticmethod
    def auth_user(account, password):
        """根據傳入的帳號密碼找到對應的紀錄並回傳

        Args:
            account: 帳號名稱
            password: 密碼

        Returns:
            回傳 user model
        """
        user = DBSession.query(UserModel).filter_by(account=account).one_or_none()
        if user and user.verify_password(password):
            return user

    @staticmethod
    def get_latest_news(quantity):
        """傳回指定筆數的最新消息

        Args:
            quantity: 指定要撈取幾筆最新消息

        Returns:
            回傳取得的最新消息
        """
        return DBSession.query(NewsModel).order_by(NewsModel.is_pinned.desc()).order_by(NewsModel.id.desc())[:quantity]

    @staticmethod
    def get_news_list(page_number=1, quantity_per_page=20, category_id=None):
        """傳回最新消息列表

        Args:
            page_number: 指定頁數，若沒指定則回傳第一頁
            quantity_per_page: 指定每頁的筆數，預設為 20 筆
            category_id: 指定要撈取的最新消息分類，None 代表不指定

        Returns:
            回傳最新消息列表
        """
        results = DBSession.query(NewsModel)
        if category_id:
            results = results.filter_by(category_id=category_id)
        now = datetime.now()
        # 只顯示在發佈時間內的最新消息
        results = (results.filter(or_(NewsModel.visible_start_date == None, now >= NewsModel.visible_start_date))
                          .filter(or_(NewsModel.visible_end_date == None, now < NewsModel.visible_end_date)))
        return (results.order_by(NewsModel.is_pinned.desc(), NewsModel.id.desc())
                   [(page_number-1)*quantity_per_page : (page_number-1)*quantity_per_page+quantity_per_page])

    @staticmethod
    def get_news_category_list():
        """回傳最新消息分類列表"""
        return DBSession.query(NewsCategoryModel).order_by(NewsCategoryModel.order)

    @staticmethod
    def get_page_quantity_of_total_news(quantity_per_page, category_id=None):
        """回傳最新消息總共有幾頁

        Args:
            quantity_per_page: 每頁幾筆最新消息
            category_id: 若有指定，則只會傳回符合此分類的最新消息頁數

        Returns:
            回傳總共頁數
        """
        results = DBSession.query(func.count(NewsModel.id))
        if category_id:
            results = results.filter_by(category_id=category_id)
        return math.ceil(results.scalar()/quantity_per_page)

    @staticmethod
    def get_site_config_list():
        """傳回系統相關的設定檔，都是以 site_ 開頭的"""
        return (DBSession.query(ConfigModel)
                         .filter(ConfigModel.name.startswith('site_'))
                         .all())

    @staticmethod
    def get_current_theme():
        """回傳目前使用的樣板名稱

        Returns:
            回傳目前的樣板名稱
        """
        return DBSession.query(ConfigModel.value).filter_by(name='site_theme').one().value

    @staticmethod
    def get_theme_list():
        """回傳所有樣板名稱列表

        Returns:
            樣板名稱列表
        """
        return DBSession.query(ThemeConfigModel.id, ThemeConfigModel.name)

    @staticmethod
    def get_theme_config(theme_name):
        """根據傳入的 theme_name 傳回佈景主題設定檔

        Args:
            theme_name: 佈景主題的名稱

        Returns:
            佈景主題設定資料結構，會將存在資料庫中的 json 格式轉成 python 的資料型別
        """
        return json.loads((DBSession.query(ThemeConfigModel)
                                    .filter_by(name=theme_name)
                                    .one()).value)

    @staticmethod
    def save_theme_config(config):
        """將傳入的 config 資料結構直接存入 theme_config 資料表

        Args:
            config: 設定檔的資料結構，由樣板自帶的 config.json 藉由 json.loads 轉換而成

        Returns:
            None
        """
        theme_config = ThemeConfigModel(name=config['name'], value=json.dumps(config, ensure_ascii=False))
        DBSession.add(theme_config)

    @staticmethod
    def create_user():
        """建立使用者物件並回傳

        Returns:
            回傳使用者物件
        """
        return UserModel()

    @staticmethod
    def get_user_account(account):
        """根據傳入的使用者帳號找到該物件並回傳

        Args:
            account: 使用者帳號名稱

        Returns:
            回傳使用者物件
        """
        return DBSession.query(UserModel).filter_by(account=account).one_or_none()

    @staticmethod
    def get_user(user_id):
        """取得使用者物件並回傳

        Args:
            user_id: UserModel.id

        Returns:
            回傳使用者物件
        """
        return DBSession.query(UserModel).get(user_id)

    @staticmethod
    def save_user(user):
        """將 UserModel 物件存至 DB

        Args:
            user: UserModel 實體

        Returns:
            None
        """
        DBSession.add(user)

    @staticmethod
    def delete_user(user):
        """將 UserModel 物件刪除

        Args:
            user: UserModel 實體

        Returns:
            None
        """
        DBSession.delete(user)

    @staticmethod
    def get_group_list():
        """傳回使用者的群組列表

        排序的依據讓同一個父群組的群組排在一起，再來才是以 order 為排序依據，這樣在 view 的階段就不用再特別處理排序
        """
        return DBSession.query(GroupModel).order_by(GroupModel.ancestor_id, GroupModel.order).all()

    @staticmethod
    def get_staff_group_list(user_id):
        """取得指定 user id 的所屬行政群組 (group type 為 tp_yass.enum.GroupType.STAFF)。最高管理者也視做是行政群組

        Args:
            user_id: UserModel 的 primary key

        Returns:
            回傳行政群組列表
        """
        return (DBSession.query(GroupModel)
                         .join(UserModel, GroupModel.users)
                         .filter(UserModel.id==user_id, GroupModel.type.in_((GroupType.ADMIN.value, GroupType.STAFF.value))))

    @staticmethod
    def get_groups(group_id_list):
        """根據傳入的 group id 列表回傳多個群組物件

        Args:
            group_id_list: 包含 GroupModel.id 的 list

        Returns:
            回傳符合的群組物件列表
        """

        return DBSession.query(GroupModel).filter(GroupModel.id.in_(group_id_list)).all()

    @staticmethod
    def get_group(group_id):
        """根據傳入的 group_id 回傳群組物件

        Args:
            group_id: 群組的 pk

        Returns:
            回傳群組物件或 None
        """
        return DBSession.query(GroupModel).get(group_id)

    @staticmethod
    def get_group_by_name(name):
        """根據傳入的群組名稱回傳對應的群組物件

        Args:
            name: 群組名稱

        Returns:
            回傳群組物件
        """
        return DBSession.query(GroupModel).filter_by(name=name).one_or_none()

    @staticmethod
    def get_or_create_group(name):
        """根據傳入的群組名稱，回傳或建立該群組

        Args:
            name: 群組名稱

        Returns:
            回傳已存在或新建立的群組
        """
        group = DAL.get_group_by_name(name)
        if not group:
            group = GroupModel(name=name)
        return group

    @staticmethod
    def create_group():
        """建立 GroupModel 實體

        Returns:
            GroupModel 實體
        """
        return GroupModel()

    @staticmethod
    def save_group(group):
        """將 UserModel 物件存至 DB

        Args:
            user: GroupModel 實體

        Returns:
            None
        """
        DBSession.add(group)

    @staticmethod
    def change_group_ancestor_id(old_ancestor_id, new_ancestor_id):
        """將原本 ancestor_id 為 old_ancestor_id 的 records 改成新的 new_ancestor_id

        Args:
            old_ancestor_id: 作為篩選條件，找出 ancestor_id 為此值的 records
            new_ancestor_id: 將找到的 records 其 ancestor_id 改成此值

        Returns:
            None
        """
        (DBSession.query(GroupModel)
                  .filter_by(ancestor_id=old_ancestor_id)
                  .update({GroupModel.ancestor_id: new_ancestor_id}))

    @staticmethod
    def delete_group(group):
        """刪除指定的 group

        Args:
            group: group 物件
        """
        DBSession.delete(group)

    @staticmethod
    def get_user_list(page=1, quantity_per_page=20, group_id=None):
        """傳回使用者列表

        Args:
            page: 指定頁數，若沒指定則回傳第一頁
            quantity_per_page: 指定每頁的筆數，預設為 20 筆
            group_id: 指定要撈取的使用者群組，None 代表不指定

        Returns:
            回傳使用者列表
        """
        results = DBSession.query(UserModel)
        if group_id:
            results = results.filter_by(group_id=group_id)
        return (results.order_by(UserModel.id.desc())
                   [(page-1)*quantity_per_page : (page-1)*quantity_per_page+quantity_per_page])

    @staticmethod
    def get_page_quantity_of_total_users(quantity_per_page, group_id=None):
        """回傳使用者列表總共有幾頁

        Args:
            quantity_per_page: 每頁幾筆最新消息
            group_id: 若有指定，則只會傳回符合此群組的使用者頁數

        Returns:
            回傳總共頁數
        """
        results = DBSession.query(func.count(UserModel.id))
        if group_id:
            results = results.filter_by(group_id=group_id)
        return math.ceil(results.scalar()/quantity_per_page)

    @staticmethod
    def get_navbar_list(type='all', visible_only=False, excluded_id=None):
        """傳回導覽列列表

        排序的依據讓同一個父群組的群組排在一起，再來才是以 order 為排序依據，這樣在 view 的階段就不用再特別處理排序

        Args:
            type: 產生的 navbar list 類型，若為 intermediate 則只傳回可接受子選單的選單物件，若為 all 則回傳全部
            visible_only: 是否只擷取 is_visible 為 True 的導覽列，預設行為是全部擷取
            excluded_id: 用來排除指定的 navbar 物件，避免後台產生建立導覽列樹狀的顯示列表時讓 UI 產生自己的上層可以指給自己的錯誤

        Returns:
            回傳排序後的 navbar list
        """
        results = DBSession.query(NavbarModel)
        if type == 'intermediate':
            results = results.filter_by(type=1)
        if visible_only:
            results = results.filter_by(is_visible=1)
        if excluded_id:
            results = results.filter(NavbarModel.id!=excluded_id)

        return results.order_by(NavbarModel.ancestor_id, NavbarModel.order).all()

    @staticmethod
    def create_navbar(form_data):
        """建立 navbar 物件

        Args:
            form_data: wtforms.forms.Form
        """
        navbar = NavbarModel()
        return DAL.sync_navbar(form_data, navbar)

    @staticmethod
    def sync_navbar(form_data, navbar):
        # 如果是內建模組，只處理幾個可以更動的設定，其他的不給變動
        if navbar.type and navbar.type in (NavbarType.BUILTIN_NEWS,
                                           NavbarType.BUILTIN_TELEXT,
                                           NavbarType.BUILTIN_LINKS):
            navbar.is_visible = 1 if form_data.is_visible.data else 0
            navbar.order = form_data.order.data
            ancestor_navbar = DAL.get_navbar(int(form_data.ancestor_id.data))
            if ancestor_navbar:
                navbar.ancestor = ancestor_navbar
            else:
                logger.error('找不到上層選單物件 %s', form_data.ancestor_id.data)
                return False
            DBSession.add(navbar)
            return True
        # 一般化的 navbar
        if form_data.type.data == NavbarType.TREE_NODE.value:
            # intermediate node
            navbar.type = NavbarType.TREE_NODE.value
            navbar.name = form_data.name.data
            if form_data.icon.data:
                navbar.icon = form_data.icon.data
            if form_data.aria_name.data:
                navbar.aria_name = form_data.aria_name.data
            else:
                logger.error('intermediate node 應該設定無障礙英文名稱')
                return False
        elif form_data.type.data == NavbarType.LEAF_NODE.value:
            # leaf node
            navbar.type = NavbarType.LEAF_NODE.value
            navbar.name = form_data.name.data
            if int(form_data.leaf_type.data) == 1:
                if form_data.page_id.data:
                    page = DAL.get_page(int(form_data.page_id.data))
                    if page:
                        navbar.page = page
                        navbar.url = None
                    else:
                        logger.error('找不到 page id 為 %s 的物件', form_data.page_id.data)
                        return False
                else:
                    logger.error('沒有指定連結的 page id')
                    return False
            elif int(form_data.leaf_type.data) == 2:
                if form_data.url.data:
                    navbar.url = form_data.url.data
                    navbar.page = None
                else:
                    logger.error('沒有指定連結的網址')
                    return False
            navbar.is_href_blank = 1 if form_data.is_href_blank.data else 0
            if form_data.icon.data:
                navbar.icon = form_data.icon.data
        elif form_data.type.data == NavbarType.DROPDOWN_DIVIDER.value:
            # divider
            navbar.type = NavbarType.DROPDOWN_DIVIDER.value
            navbar.name = '分隔線'
        navbar.is_visible = 1 if form_data.is_visible.data else 0
        navbar.order = form_data.order.data
        ancestor_navbar = DAL.get_navbar(int(form_data.ancestor_id.data))
        if ancestor_navbar:
            navbar.ancestor = ancestor_navbar
        else:
            logger.error('找不到上層選單物件 %s', form_data.ancestor_id.data)
            return False
        DBSession.add(navbar)
        return True

    @staticmethod
    def get_navbar(navbar_id):
        """取得導覽列物件

        Args:
            navbar_id: NavbarModel 的 primary key

        Returns:
            回傳導覽列物件
        """
        return DBSession.query(NavbarModel).get(navbar_id)

    @staticmethod
    def change_navbar_ancestor_id(old_ancestor_id, new_ancestor_id):
        """將原本 ancestor_id 為 old_ancestor_id 的 records 改成新的 new_ancestor_id

        Args:
            old_ancestor_id: 作為篩選條件，找出 ancestor_id 為此值的 records
            new_ancestor_id: 將找到的 records 其 ancestor_id 改成此值

        Returns:
            None
        """
        (DBSession.query(NavbarModel)
         .filter_by(ancestor_id=old_ancestor_id)
         .update({NavbarModel.ancestor_id: new_ancestor_id}))

    @staticmethod
    def delete_navbar(navbar):
        """刪除指定的 navbar 物件

        Args:
            navbar: NavbarModel 物件
        """
        if navbar.type in (NavbarType.TREE_NODE,
                           NavbarType.LEAF_NODE,
                           NavbarType.DROPDOWN_DIVIDER):
            DBSession.delete(navbar)
            return True
        else:
            return False

    @staticmethod
    def update_site_config_list(updated_config_list):
        """更新 site config"""
        for each_config in updated_config_list:
            DBSession.query(ConfigModel).filter_by(id=each_config['id']).update(each_config, synchronize_session=False)
        return True

    @staticmethod
    def get_tag_by_name(name):
        """根據傳入的標籤名稱回傳對應的標籤物件

        Args:
            name: 標籤名稱

        Returns:
            回傳標籤物件
        """
        return DBSession.query(TagModel).filter_by(name=name).one_or_none()

    @staticmethod
    def get_or_create_tag(name):
        """根據傳入的標籤名稱，回傳或建立該標籤

        Args:
            name: 標籤名稱

        Returns:
            回傳已存在或新建立的標籤
        """
        tag = DAL.get_tag_by_name(name)
        if not tag:
            tag = TagModel(name=name)
        return tag

    @staticmethod
    def get_page(page_id):
        """取得指定的單一頁面

        Args:
            page_id: 單一頁面的 primary key

        Returns:
            回傳單一頁面
        """
        return DBSession.query(PageModel).get(page_id)

    @staticmethod
    def create_page(form_data):
        """建立單一頁面

        Args:
            form_data: wtforms.forms.Form 物件

        Returns:
            回傳已建立的單一頁面物件
        """
        page = PageModel(title=form_data.title.data, content=form_data.content.data)
        # 處理 tags
        tags = {each_tag.strip() for each_tag in form_data.tags.data.split(',')}
        for each_tag_name in tags:
            tag = DAL.get_or_create_tag(each_tag_name)
            page.tags.append(tag)
        # 處理 groups
        group_ids = form_data.group_ids.data
        page.groups = DAL.get_groups(group_ids)
        DBSession.add(page)
        DBSession.flush()
        return page

    @staticmethod
    def update_page(page, form_data, is_admin):
        """使用 form 的資料更新指定的單一頁面

        Args:
            page: PageModel 物件
            form_data: wtforms.forms.Form 物件
            is_admin: boolean 值，用來確認執行的身份是否為管理權限，若不是，則不更動單一頁面的管理群組設定

        Returns:
            回傳已更新的單一頁面物件
        """
        page.title = form_data.title.data
        page.content = form_data.content.data
        # 處理 tag
        page.tags = []
        tags = {each_tag.strip() for each_tag in form_data.tags.data.split(',')}
        for each_tag_name in tags:
            tag = DAL.get_or_create_tag(each_tag_name)
            page.tags.append(tag)
        # 若是管理權限，則處理單一頁面的群組
        if is_admin:
            group_ids = form_data.group_ids.data
            page.groups = DAL.get_groups(group_ids)
        return page

    @staticmethod
    def delete_page(page):
        """刪除單一頁面

        Args
            page: PageModel
        """
        DBSession.delete(page)

    @staticmethod
    def get_page(page_id):
        """取得單一頁面"""
        return DBSession.query(PageModel).get(page_id)

    @staticmethod
    def save_page(page):
        """將單一頁面物件存入 db session 中

        Args:
            page: 單一頁面物件
        """
        DBSession.add(page)

    @staticmethod
    def create_page_attachment(original_name, real_name):
        """建立單一頁面的上傳附件選單

        Args:
            original_name: 上傳檔案的原本的名稱
            real_name: 系統產生的亂入檔名

        Returns:
            回傳該單一頁面上傳附件物件
        """
        return PageAttachmentModel(original_name=original_name, real_name=real_name)

    @staticmethod
    def delete_page_attachment(page_attachment):
        """刪除指定的 PageAttachment

        Args:
            page_attachment: PageAttachment 物件
        """
        DBSession.delete(page_attachment)

    @staticmethod
    def get_page_quantity_of_total_pages(quantity_per_page, group_id=None):
        """回傳單一頁面列表總共有幾頁

        Args:
            quantity_per_page: 每頁幾筆單一頁面
            group_id: 若有指定，則只會傳回符合此群組的單一頁面頁數

        Returns:
            回傳總共頁數
        """
        results = DBSession.query(func.count(PageModel.id))
        if group_id:
            results = results.filter(GroupModel.id==group_id)
        return math.ceil(results.scalar()/quantity_per_page)

    @staticmethod
    def get_page_list(page_number=1, quantity_per_page=20, group_id=None, pagination=True):
        """傳回使用者列表

        Args:
            page_number: 指定頁數，若沒指定則回傳第一頁
            quantity_per_page: 指定每頁的筆數，預設為 20 筆
            group_id: 指定要撈取的使用者群組，None 代表不指定
            pagination: 代表是否要分頁，預設為要分頁，若為 False 代表不分頁傳回全部的單一頁面

        Returns:
            回傳使用者列表
        """
        results = DBSession.query(PageModel)
        if group_id:
            results = results.filter(GroupModel.id == group_id)
        if pagination:
            return (results.order_by(PageModel.id.desc())
                        [(page_number-1)*quantity_per_page : (page_number-1)*quantity_per_page+quantity_per_page])
        else:
            return results.all()

    @staticmethod
    def get_news_category(category_id):
        """取得指定的 news category 物件

        Args:
            category_id: news category 的 id

        Returns:
            回傳 NewsCategory 物件
        """
        return DBSession.query(NewsCategoryModel).get(category_id)

    @staticmethod
    def create_news(form_data):
        """建立最新消息

        Args:
            form_data: wtforms.forms.Form 物件

        Returns:
            回傳已建立的最新消息物件
        """
        news = NewsModel(title=form_data.title.data,
                         content=form_data.content.data,
                         group_id=form_data.group_id.data,
                         category_id=form_data.category_id.data)

        # 處理置頂的邏輯，如果勾選了置頂，先確認是否有指定起訖時間，再檢查後者要比前者晚，
        # 若現在是置頂期間，才將 is_pinned 設為 1 否則為 0 等待 cronjob 處理
        if form_data.is_pinned.data:
            news.pinned_start_date = form_data.pinned_start_date.data
            news.pinned_end_date = form_data.pinned_end_date.data
            today = date.today()
            if news.pinned_start_date <= today <= news.pinned_end_date:
                news.is_pinned = 1
            else:
                news.is_pinned = 0

        if form_data.visible_start_date.data:
            news.visible_start_date = form_data.visible_start_date.data
        if form_data.visible_end_date.data:
            news.visible_end_date = form_data.visible_end_date.data

        # 處理 tags
        tags = {each_tag.strip() for each_tag in form_data.tags.data.split(',')}
        for each_tag_name in tags:
            tag = DAL.get_or_create_tag(each_tag_name)
            news.tags.append(tag)

        DBSession.add(news)
        DBSession.flush()

        return news

    @staticmethod
    def create_news_attachment(original_name, real_name):
        """建立最新消息的上傳附件選單

        Args:
            original_name: 上傳檔案的原本的名稱
            real_name: 系統產生的亂入檔名

        Returns:
            回傳該單一頁面上傳附件物件
        """
        return NewsAttachmentModel(original_name=original_name, real_name=real_name)

    @staticmethod
    def save_news(news):
        """將最新消息物件存入 db session 中

        Args:
            page: 最新消息物件
        """
        DBSession.add(news)

    @staticmethod
    def get_news(news_id):
        """取得 NewsModel 物件

        Args:
            news_id: news 的 primary key

        Returns:
            回傳 NewsModel
        """
        return DBSession.query(NewsModel).get(news_id)

    @staticmethod
    def delete_news(news):
        """刪除最新消息

        Args:
            news: NewsModel
        """
        DBSession.delete(news)

    @staticmethod
    def update_news(news, form_data):
        """使用 form 的資料更新指定的最新消息

        Args:
            news: NewsModel 物件
            form_data: wtforms.forms.Form 物件

        Returns:
            回傳已更新的最新消息物件
        """
        news.title = form_data.title.data
        news.content = form_data.content.data
        news.group_id = form_data.group_id.data
        news.category_id = form_data.category_id.data

        # 處理置頂的邏輯，如果勾選了置頂，先確認是否有指定起訖時間，再檢查後者要比前者晚，
        # 若現在是置頂期間，才將 is_pinned 設為 1 否則為 0 等待 cronjob 處理
        if form_data.is_pinned.data:
            news.pinned_start_date = form_data.pinned_start_date.data
            news.pinned_end_date = form_data.pinned_end_date.data
            today = date.today()
            if news.pinned_start_date <= today <= news.pinned_end_date:
                news.is_pinned = 1
            else:
                news.is_pinned = 0

        if form_data.visible_start_date.data:
            news.visible_start_date = form_data.visible_start_date.data
        if form_data.visible_end_date.data:
            news.visible_end_date = form_data.visible_end_date.data

        # 處理 tags
        tags = {each_tag.strip() for each_tag in form_data.tags.data.split(',')}
        for each_tag_name in tags:
            tag = DAL.get_or_create_tag(each_tag_name)
            news.tags.append(tag)

        DBSession.add(news)

        return news

    @staticmethod
    def delete_news_attachment(news_attachment):
        """刪除指定的 NewsAttachment

        Args:
            news_attachment: NewsAttachment 物件
        """
        DBSession.delete(news_attachment)

    @staticmethod
    def create_news_category(form_data):
        """建立最新消息的分類

        Args:
            form_data: wtforms.forms.Form

        Returns:
            回傳建立的 news category
        """
        news_category = NewsCategoryModel()
        form_data.populate_obj(news_category)
        DBSession.add(news_category)

    @staticmethod
    def get_page_quantity_of_total_news_categories(quantity_per_page):
        """回傳最新消息分頁總共有幾頁

        Args:
            quantity_per_page: 每頁幾筆最新消息分類

        Returns:
            回傳總共頁數
        """
        results = DBSession.query(func.count(NewsCategoryModel.id))
        return math.ceil(results.scalar() / quantity_per_page)

    @staticmethod
    def delete_news_category(news_category_id):
        """刪除指定的最新消息分類

        Args:
            news_category_id: 最新消息分類的 primary key

        Returns:
            若回傳 False 代表該分類還有相依的最新消息
        """
        try:
            DBSession.query(NewsCategoryModel).filter_by(id=news_category_id).delete()
            return True
        except IntegrityError:
            return False

    @staticmethod
    def update_news_category(news_category, form_data):
        """使用 form 的資料更新指定的最新消息

        Args:
            news_category: NewsCategoryModel 物件
            form_data: wtforms.forms.Form 物件

        Returns:
            回傳已更新的最新消息分類物件
        """
        form_data.populate_obj(news_category)
        DBSession.add(news_category)

    @staticmethod
    def get_link(link_id):
        """取得 LinkModel 物件

        Args:
            link_id: LinkModel 的 primary key

        Returns:
            回傳 LinkModel 物件
        """
        return DBSession.query(LinkModel).get(link_id)

    @staticmethod
    def get_link_category_list():
        """回傳好站連結分類列表"""
        return DBSession.query(LinkCategoryModel).order_by(LinkCategoryModel.order)

    @staticmethod
    def create_link(form_data):
        """建立好站連結

        Args:
            form_data: wtforms.forms.Form 物件

        Returns:
            回傳已建立的好站連結物件
        """
        link = LinkModel(title=form_data.title.data,
                         url=form_data.url.data,
                         icon='',
                         group_id=form_data.group_id.data,
                         category_id=form_data.category_id.data)

        link.is_pinned = True if form_data.is_pinned.data else False
        DBSession.add(link)
        DBSession.flush()
        return link

    @staticmethod
    def save_link(link):
        """儲存 link model

        Args:
            link: LinkModel 物件
        """
        DBSession.add(link)

    @staticmethod
    def get_link_list(page_number=1, quantity_per_page=20, category_id=None):
        """傳回好站連結列表

        Args:
            page_number: 指定頁數，若沒指定則回傳第一頁
            quantity_per_page: 指定每頁的筆數，預設為 20 筆
            category_id: 指定要撈取的好站連結分類，None 代表不指定

        Returns:
            回傳好站連結列表
        """
        results = DBSession.query(LinkModel)
        if category_id:
            results = results.filter_by(category_id=category_id)
        return (results.order_by(LinkModel.is_pinned.desc(), LinkModel.id.desc())
                    [(page_number - 1) * quantity_per_page: (page_number - 1) * quantity_per_page + quantity_per_page])

    @staticmethod
    def get_pinned_link_list():
        """取得需要顯示在首頁上的好站連結"""
        return DBSession.query(LinkModel).filter_by(is_pinned=1)

    @staticmethod
    def get_page_quantity_of_total_link(quantity_per_page, category_id=None):
        """回傳好站連結總共有幾頁

        Args:
            quantity_per_page: 每頁幾筆最新消息
            category_id: 若有指定，則只會傳回符合此分類的好站連結頁數

        Returns:
            回傳總共頁數
        """
        results = DBSession.query(func.count(LinkModel.id))
        if category_id:
            results = results.filter_by(category_id=category_id)
        return math.ceil(results.scalar() / quantity_per_page)

    @staticmethod
    def delete_link(link):
        """刪除好站連結

        Args:
            link: LinkModel
        """
        DBSession.delete(link)

    @staticmethod
    def update_link(link, form_data):
        """使用 form 的資料更新指定的好站連結

        Args:
            link: LinkModel 物件
            form_data: wtforms.forms.Form 物件
        """
        link.title = form_data.title.data
        link.url = form_data.url.data
        link.is_pinned = 1 if form_data.is_pinned.data else 0
        return link

    @staticmethod
    def save_link(link):
        """將好站連結物件存入 db session 中

        Args:
            link: 好站連結物件
        """
        DBSession.add(link)

    @staticmethod
    def create_link_category(form_data):
        """建立好站連結的分類

        Args:
            form_data: wtforms.forms.Form

        Returns:
            回傳建立的 link category
        """
        link_category = LinkCategoryModel()
        form_data.populate_obj(link_category)
        DBSession.add(link_category)

    @staticmethod
    def get_page_quantity_of_total_link_categories(quantity_per_page):
        """回傳好站連結分頁總共有幾頁

        Args:
            quantity_per_page: 每頁幾筆好站連結分類

        Returns:
            回傳總共頁數
        """
        results = DBSession.query(func.count(LinkCategoryModel.id))
        return math.ceil(results.scalar() / quantity_per_page)

    @staticmethod
    def delete_link_category(link_category_id):
        """刪除指定的好站連結分類

        Args:
            link_category_id: 好站連結分類的 primary key

        Returns:
            若回傳 False 代表該分類還有相依的好站連結
        """
        try:
            DBSession.query(LinkCategoryModel).filter_by(id=link_category_id).delete()
            return True
        except IntegrityError:
            return False

    @staticmethod
    def get_link_category_list():
        """回傳好站連結分類列表"""
        return DBSession.query(LinkCategoryModel).order_by(LinkCategoryModel.order)

    @staticmethod
    def update_link_category(link_category, form_data):
        """使用 form 的資料更新指定的好站連結

        Args:
            link_category: LinkCategoryModel 物件
            form_data: wtforms.forms.Form 物件

        Returns:
            回傳已更新的好站連結分類物件
        """
        form_data.populate_obj(link_category)
        DBSession.add(link_category)

    @staticmethod
    def get_link_category(category_id):
        """取得指定的 link category 物件

        Args:
            category_id: link category 的 id

        Returns:
            回傳 LinkCategory 物件
        """
        return DBSession.query(LinkCategoryModel).get(category_id)

    @staticmethod
    def get_page_quantity_of_total_links(quantity_per_page, category_id=None):
        """回傳好站連結總共有幾頁

        Args:
            quantity_per_page: 每頁幾筆好站連結
            category_id: 若有指定，則只會傳回符合此分類的好站連結頁數

        Returns:
            回傳總共頁數
        """
        results = DBSession.query(func.count(LinkModel.id))
        if category_id:
            results = results.filter_by(category_id=category_id)
        return math.ceil(results.scalar() / quantity_per_page)

    @staticmethod
    def create_telext(form_data):
        """建立分機表

        Args:
            form_data: wtforms.forms.Form
        """
        telext = TelExtModel()
        form_data.populate_obj(telext)
        telext.is_pinned = 1 if form_data.is_pinned.data else 0
        DBSession.add(telext)

    @staticmethod
    def get_telext_list():
        """回傳分機表列表"""
        return DBSession.query(TelExtModel).order_by(TelExtModel.order)

    @staticmethod
    def get_pinned_telext_list():
        """回傳根據 order 排序指定顯示在首頁的分機表"""
        return (DBSession.query(TelExtModel)
                .filter_by(is_pinned=1)
                .order_by(TelExtModel.order))

    @staticmethod
    def delete_telext(telext_id):
        """刪除分機

        Args:
            telext_id: TelExtModel 的 primary key
        """
        DBSession.query(TelExtModel).filter_by(id=telext_id).delete()

    @staticmethod
    def update_telext(telext_id, form_data):
        """更新分機表

        Args:
            telext_id: 分機表 TelExtModel 的 primary key
            form_data: wtforms.forms.Form
        """
        telext = DBSession.query(TelExtModel).get(telext_id)
        form_data.populate_obj(telext)
        telext.is_pinned = 1 if form_data.is_pinned.data else 0
        DBSession.add(telext)
        return True

    @staticmethod
    def get_telext(telext_id):
        """取得分機

        Args:
            telext_id: 分機表 TelExtModel 的 primary key
        """
        return DBSession.query(TelExtModel).get(telext_id)

    @staticmethod
    def log_auth(auth_log_type, user_id, client_addr):
        """紀錄使用者的認証

        Args:
            auth_log_type: enum.AuthLogType
            user_id: 使用者的 id
            client_addr: 來源端的 ip 位址
        """
        auth_log = AuthLogModel(type=int(auth_log_type), user_id=user_id, client_addr=client_addr)
        DBSession.add(auth_log)

    @staticmethod
    def get_auth_log_list(page_number=1, quantity_per_page=20, user_id=None):
        """傳回 auth log 紀錄列表

        Args:
            page_number: 指定頁數，若沒指定則回傳第一頁
            quantity_per_page: 指定每頁的筆數，預設為 20 筆
            user_id: 指定要撈取的使用者 auth log，None 代表全部撈出

        Returns:
            回傳 auth log 列表
        """
        results = DBSession.query(AuthLogModel)
        if user_id:
            results = results.filter_by(user_id=user_id)
        return (results.order_by(AuthLogModel.id.desc())
                   [(page_number-1)*quantity_per_page : (page_number-1)*quantity_per_page+quantity_per_page])

    @staticmethod
    def get_page_quantity_of_total_auth_logs(quantity_per_page, user_id=None):
        """回傳 auth logs 總共有幾頁

        Args:
            quantity_per_page: 每頁幾筆最新消息
            user_id: 若有指定，則只會根據指定 user id 的 auth logs 去計算頁數

        Returns:
            回傳總共頁數
        """
        results = DBSession.query(func.count(AuthLogModel.id))
        if user_id:
            results = results.filter_by(user_id=user_id)
        return math.ceil(results.scalar()/quantity_per_page)
