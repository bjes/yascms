from datetime import datetime

from sqlalchemy import (Column,
                        Integer,
                        String,
                        Date,
                        DateTime,
                        Text,
                        ForeignKey)
from sqlalchemy.orm import relationship
from pyramid_sqlalchemy import BaseObject


class LinkModel(BaseObject):
    """好站連結"""

    __tablename__ = 'links'

    id = Column(Integer, primary_key=True)

    # 標題
    title = Column(String(100), nullable=False, index=True)

    # 連結網址
    url = Column(Text, nullable=False)

    # 上傳圖檔的名稱
    icon = Column(String(100), nullable=False)

    # 是否顯示在釘選在首頁
    is_pinned = Column(Integer, nullable=False, default=0, server_default='0')

    # 發佈時間，建立這篇好站連結當下的時間
    publication_date = Column(DateTime, nullable=False, default=datetime.now)

    # 最後更新時間
    last_updated_date = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # 可編輯此好站連結的群組
    group_id = Column(Integer, ForeignKey('groups.id'))

    category_id = Column(Integer, ForeignKey('link_categories.id'))


class LinCategoryModel(BaseObject):
    """好站連結分類"""

    __tablename__ = 'link_categories'

    id = Column(Integer, primary_key=True)

    # 分類名稱
    name = Column(String(50), unique=True, nullable=False)

    # 排序
    order = Column(Integer, nullable=False, default=0, server_default='0')

    links = relationship(LinkModel, backref='category')
