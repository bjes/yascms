from sqlalchemy import Column, Integer, String, Text
from pyramid_sqlalchemy import BaseObject


class SysConfigModel(BaseObject):
    '''存放系統設定值'''

    __tablename__ = 'sys_config'

    id = Column(Integer, primary_key=True)

    # 設定名稱
    name= Column(String(50), nullable=False)

    # 設定值
    value = Column(Text, nullable=False)

    # 說明文字
    description = Column(String(50), nullable=False)
