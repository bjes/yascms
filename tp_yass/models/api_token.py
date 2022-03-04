from sqlalchemy import Column, Integer, String, Text
from pyramid_sqlalchemy import BaseObject


class APITokenModel(BaseObject):
    """存放 api token 的設定"""

    __tablename__ = 'api_tokens'

    id = Column(Integer, primary_key=True)

    # 設定 api token 名稱
    name= Column(String(50), nullable=False, unique=True)

    # 說明
    description = Column(Text)

    # 設定值
    value = Column(Text, nullable=False)
