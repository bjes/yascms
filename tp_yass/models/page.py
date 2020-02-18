from pyramid_sqlalchemy import BaseObject
from sqlalchemy import (Column,
                        String,
                        Integer,
                        Text,
                        ForeignKey,
                        Table)
from sqlalchemy.orm import relationship

from tp_yass import models


pages_tags_association = Table('pages_tags_association',
                               BaseObject.metadata,
                               Column('page_id', Integer, ForeignKey('pages.id')),
                               Column('tag_id', Integer, ForeignKey('tags.id')))


class PageModel(BaseObject):
    """單頁網頁"""

    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True)

    # 標題
    title = Column(String(50), nullable=False)

    # 內容
    content = Column(Text, nullable=False, default='', server_default='')

    # 標籤
    tags = relationship('models.tag.TagModel', secondary=pages_tags_association, back_populates='pages')
