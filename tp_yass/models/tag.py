from pyramid_sqlalchemy import BaseObject
from sqlalchemy import (Column,
                        Integer,
                        String)
from sqlalchemy.orm import relationship

from tp_yass import models


class TagModel(BaseObject):
    """標籤"""

    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)

    name = Column(String(50), nullable=False)

    news = relationship('models.news.NewsModel', secondary=models.news.news_tags_association, back_populates='tags')
    pages = relationship('models.page.PageModel', secondary=models.page.pages_tags_association, back_populates='tags')
