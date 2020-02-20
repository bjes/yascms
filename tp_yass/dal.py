"""資料庫存取抽象層

為了避免 views 相依 orm 操作，所以抽象資料存取層
"""
import math
from datetime import datetime

from sqlalchemy import or_, func
from pyramid_sqlalchemy import Session as DBSession

from tp_yass.models.sys_config import SysConfigModel
from tp_yass.models.user import UserModel, GroupModel
from tp_yass.models.news import NewsModel, NewsCategoryModel
from tp_yass.models.navbar import NavbarModel
from tp_yass.models.sys_config import SysConfigModel


class DAL:

    @staticmethod
    def get_user(account, password):
        """根據傳入的帳號密碼找到對應的紀錄並回傳"""
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
    def get_news_list(page=1, quantity_per_page=20, category_id=None):
        """傳回最新消息列表

        Args:
            page: 指定頁數，若沒指定則回傳第一頁
            quantity_per_page: 指定每頁的筆數，預設為 20 筆
            category_id: 指定要撈取的最新消息分類，None 代表不指定
        """
        results = DBSession.query(NewsModel)
        if category_id:
            results = results.filter_by(category_id=category_id)
        now = datetime.now()
        # 只顯示在發佈時間內的最新消息
        results = (results.filter(now >= NewsModel.visible_start_date)
                   .filter(or_(NewsModel.visible_end_date == None, now < NewsModel.visible_end_date)))
        return (results.order_by(NewsModel.is_pinned.desc(), NewsModel.id.desc())
                   [(page-1)*quantity_per_page : (page-1)*quantity_per_page+quantity_per_page])

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
    def get_sys_config_list():
        """傳回系統設定檔"""
        return DBSession.query(SysConfigModel).all()

    @staticmethod
    def get_user_group_list():
        """傳回使用者的群組列表

        排序的依據讓同一個父群組的群組排在一起，再來才是以 order 為排序依據，這樣在 view 的階段就不用再特別處理排序
        """
        return DBSession.query(GroupModel).order_by(GroupModel.ancestor_id, GroupModel.order).all()

    @staticmethod
    def get_user_list(page=1, quantity_per_page=20, group_id=None):
        """傳回使用者列表

        Args:
            page: 指定頁數，若沒指定則回傳第一頁
            quantity_per_page: 指定每頁的筆數，預設為 20 筆
            group_id: 指定要撈取的使用者群組，None 代表不指定
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
    def get_navbar_list():
        """傳回導覽列列表

        排序的依據讓同一個父群組的群組排在一起，再來才是以 order 為排序依據，這樣在 view 的階段就不用再特別處理排序
        """
        return DBSession.query(NavbarModel).order_by(NavbarModel.ancestor_id, NavbarModel.order).all()

    @staticmethod
    def get_sys_config_list():
        """回傳系統設定列表

        其中 maintenance_mode 是用來升即時全站唯讀用，所以不給設定
        """
        return (DBSession.query(SysConfigModel)
                         .filter(SysConfigModel.name != 'maintenance_mode')
                         .order_by(SysConfigModel.id))

    @staticmethod
    def update_sys_config_list(updated_config_list):
        """更新 sys config"""
        for each_config in updated_config_list:
            DBSession.query(SysConfigModel).filter_by(id=each_config['id']).update(each_config, synchronize_session=False)
        return True
