from datetime import datetime

from sqlalchemy import (Column,
                        Integer,
                        String,
                        Boolean,
                        DateTime,
                        Text,
                        ForeignKey)
from sqlalchemy.orm import relationship
from pyramid_sqlalchemy import BaseObject


class NewsAttachmentModel(BaseObject):
    '''news 的上傳附檔'''

    __tablename__ = 'news_attachments'

    id = Column(Integer, primary_key=True)

    # 上傳時原本的檔案名稱
    original_name = Column(String(100), nullable=False)

    # 儲存至硬碟上的檔案名稱
    real_name = Column(String(100), nullable=False)

    news_id = Column(Integer, ForeignKey('news.id'))


class NewsModel(BaseObject):

    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)

    title = Column(String(100), nullable=False, index=True)

    content = Column(Text, nullable=False, default='')

    attachments = relationship('NewsAttachmentModel', backref='news')

    # 是否置頂，預設為 0 (否)
    is_pinned = Column(Integer, default=0, server_default='0')

    # 置頂開始時間
    pinned_start_date = Column(DateTime, nullable=True)

    # 置頂結束時間
    pinned_end_date = Column(DateTime, nullable=True)

    # 顯示開始時間，時間到了才會顯示在網頁上
    visible_start_date = Column(DateTime, nullable=False, default=datetime.now)

    # 顯示結束時間，時間到了才會消失在網頁上。若沒指定 (null) 則代表永久顯示
    visible_end_date = Column(DateTime, nullable=True)

    # 發佈時間，建立這篇最新消息當下的時間
    publication_date = Column(DateTime, nullable=False, default=datetime.now)

    # 最後更新時間
    last_updated_date = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    group_id = Column(Integer, ForeignKey('groups.id'))

    category_id = Column(Integer, ForeignKey('news_categories.id'))


class NewsCategoryModel(BaseObject):

    __tablename__ = 'news_categories'

    id = Column(Integer, primary_key=True)

    name = Column(String(50), nullable=False)

    # 排序
    order = Column(Integer, nullable=False, default=0, server_default='0')

    news = relationship(NewsModel, backref='category')
