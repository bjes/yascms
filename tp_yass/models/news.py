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

    attachments = relationship('NewsAttachment', backref='news')

    # 是否置頂，預設為否
    is_pinned = Column(Boolean, default=False, server_default='0')

    # 發佈時間
    publication_date = Column(DateTime, nullable=False, default=datetime.now)

    # 最後更新時間
    last_updated_date = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    group_id = Column(Integer, ForeignKey('groups.id'))
