from sqlalchemy import Column, Integer, String

from pyramid_sqlalchemy import BaseObject


class HomepageOrderModel(BaseObject):
    """用來處理首頁排序"""

    __tablename__ = 'homepage_order'

    id = Column(Integer, primary_key=True)

    # 自訂簡短名稱
    name = Column(String(50))

    # 類型，目前可以接受的類型定義在 tp_yass.enum.HomepageOrderType
    type = Column(Integer, nullable=False)

    # 子類型，目前只有最新消息和好站連結，可以指定子類型，用來讓首頁顯示特定類型的內容。
    # 0 代表沒有指定全部顯示
    sub_type = Column(Integer, nullable=True)

    # 要撈取的數量，比方最新消息要撈幾筆資料顯示在首頁
    quantity = Column(Integer, nullable=False)

    # 詳細說明
    description = Column(String(100))

    # 排序，若沒指定則預設為 0 ，代表以 primary key 排序
    order = Column(Integer, nullable=False, default=0, server_default='0')
