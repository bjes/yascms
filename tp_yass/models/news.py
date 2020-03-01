from datetime import datetime

from sqlalchemy import (Column,
                        Integer,
                        String,
                        DateTime,
                        Date,
                        Text,
                        ForeignKey,
                        Table)
from sqlalchemy.orm import relationship
from pyramid_sqlalchemy import BaseObject


news_tags_association = Table('news_tags_association',
                              BaseObject.metadata,
                              Column('news_id', Integer, ForeignKey('news.id')),
                              Column('tag_id', Integer, ForeignKey('tags.id')))


class NewsAttachmentModel(BaseObject):
    """news 的上傳附檔"""

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

    # 標題
    title = Column(String(100), nullable=False, index=True)

    # 內容
    content = Column(Text, nullable=False, default='', server_default='')

    # 上傳附件
    attachments = relationship('NewsAttachmentModel', backref='news', cascade='all, delete-orphan')

    # 是否置頂
    is_pinned = Column(Integer, nullable=False, default=0, server_default='0')

    # 置頂開始時間
    pinned_start_date = Column(Date)

    # 置頂結束時間
    pinned_end_date = Column(Date)

    # 顯示開始時間，時間到了才會顯示在網頁上。若沒指定（null）則代表馬上顯示
    visible_start_date = Column(DateTime)

    # 顯示結束時間，時間到了才會消失在網頁上。若沒指定 (null) 則代表永久顯示
    visible_end_date = Column(DateTime)

    # 發佈時間，建立這篇最新消息當下的時間
    publication_date = Column(DateTime, nullable=False, default=datetime.now)

    # 最後更新時間
    last_updated_date = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # 標籤
    tags = relationship('models.tag.TagModel', secondary=news_tags_association, back_populates='news')

    group_id = Column(Integer, ForeignKey('groups.id'))

    category_id = Column(Integer, ForeignKey('news_categories.id'))


class NewsCategoryModel(BaseObject):
    """最新消息分類"""

    __tablename__ = 'news_categories'

    id = Column(Integer, primary_key=True)

    # 分類名稱
    name = Column(String(50), unique=True, nullable=False)

    # 排序
    order = Column(Integer, nullable=False, default=0, server_default='0')

    news = relationship(NewsModel, backref='category')
