from sqlalchemy import Column, Integer, String, Text

from pyramid_sqlalchemy import BaseObject


class HomepageOrderModel(BaseObject):
    """用來處理首頁排序"""

    __tablename__ = 'homepage_order'

    id = Column(Integer, primary_key=True)

    # 自訂簡短名稱
    name = Column(String(50))

    # 類型，目前可以接受的類型定義在 tp_yass.enum.HomepageOrderType
    type = Column(Integer, nullable=False)

    # 顏色

    # 參數，不同的類型會需要儲存不同的參數，以 json 格式存放
    params = Column(Text, nullable=False)

    # 詳細說明
    description = Column(String(100))

    # 排序，若沒指定則預設為 0 ，代表以 primary key 排序
    order = Column(Integer, nullable=False, default=0, server_default='0')
