from pyramid_sqlalchemy import BaseObject
from sqlalchemy import (Column,
                        Integer,
                        String)
from sqlalchemy.orm import relationship

from tp_yass.models.associations import news_tags_association, pages_tags_association


class TagModel(BaseObject):
    """標籤"""

    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)

    name = Column(String(50), unique=True, nullable=False)

    news = relationship('models.news.NewsModel', secondary=news_tags_association, back_populates='tags')
    pages = relationship('models.page.PageModel', secondary=pages_tags_association, back_populates='tags')
