from pyramid_sqlalchemy import Session as DBSession

from tp_yass.models.user import UserModel, GroupModel
from tp_yass.models.news import NewsModel
from tp_yass.models.sys_config import SysConfigModel


class DAL:

    @staticmethod
    def get_user(account, password):
        """根據傳入的帳號密碼找到對應的紀錄並回傳"""
        user = DBSession.query(UserModel).filter_by(account=account).one_or_none()
        if user and user.verify_password(password):
            return user

    @staticmethod
    def get_news_list(quantity):
        """傳回最新消息列表"""
        return DBSession.query(NewsModel).order_by(NewsModel.is_pinned.desc()).order_by(NewsModel.id.desc())[:quantity]

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
