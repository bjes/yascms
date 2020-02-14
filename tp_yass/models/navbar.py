from sqlalchemy import (Column,
                        Integer,
                        String,
                        Text,
                        ForeignKey)
from sqlalchemy.orm import relationship

from pyramid_sqlalchemy import BaseObject


class NavbarModel(BaseObject):
    """定義導覽列，其為巢狀架構"""

    __tablename__ = 'navbar'

    id = Column(Integer, primary_key=True)

    # 選單名稱
    name = Column(String(50), nullable=False, server_default='')

    # 無障礙用的名稱，只能是英文。只要不是 leaf node 都要設定此值
    aria_name = Column(String(50), nullable=True)

    # 連結的 url
    url = Column(Text, nullable=False, default='#', server_default='#')

    # 是否為外部連結，若是，點選連結時另開分頁
    is_external = Column(Integer, nullable=False, default=0, server_default='0')

    # 使用的 fontawesome icon
    icon = Column(String(50), nullable=False, default='', server_default='')

    # 選單類型， 1 為選單 （代表其下還有子選單， tree node），2 為連結 （leaf node），3 為分隔線 （dropdown divider)
    # 4 是代表為 builtin 有子選單的模組（比如最新消息），其下不可編輯； 5 是代表 builtin 沒有子選單的模組，比方行事曆
    type = Column(Integer, nullable=False)

    # 內建的模組才會用到此欄位，用來讓程式判斷這是哪一個模組，以調用該模組的選單產生
    module_name = Column(String(50), nullable=True)

    # 排序
    order = Column(Integer, nullable=False, default=0, server_default='0')

    # 是否顯示，有時候只是想暫時隱藏
    is_visible = Column(Integer, nullable=False, default=1, server_default='1')

    # self-referential relationship
    ancestor_id  = Column(Integer, ForeignKey('navbar.id'))
    ancestor = relationship('NavbarModel', backref='descendants', remote_side=[id])

