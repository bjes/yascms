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

    # 類型，文字或是整數，以便檢驗使用者有無輸入錯誤，可設定的值為 str / int / bool
    type = Column(String(5), nullable=False)

    # 說明文字
    description = Column(String(50), nullable=False)
