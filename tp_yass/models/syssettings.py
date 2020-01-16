from sqlalchemy import Column, Integer, String
from pyramid_sqlalchemy import BaseObject


class SysSettingsModel(BaseObject):

    __tablename__ = 'sys_settings'

    id = Column(Integer, primary_key=True)

    # 設定名稱
    name= Column(String(50), nullable=False)

    # 設定值
    value = Column(String(50), nullable=False)
