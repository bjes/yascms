from pyramid_sqlalchemy import BaseObject
from sqlalchemy import (Column,
                        Integer,
                        String)


class TagModel(BaseObject):
    """標籤"""

    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)

    name = Column(String(50), nullable=False)

    
