from passlib.hash import sha512_crypt
from sqlalchemy import (Column,
                        Integer,
                        String,
                        ForeignKey)
from sqlalchemy.orm import relationship
from pyramid_sqlalchemy import BaseObject

from .news import News


class User(BaseObject):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    # 名
    first_name = Column(String(20), nullable=False)

    # 姓
    last_name = Column(String(20), nullable=False)

    # 電子郵件
    email = Column(String(50), nullable=False)

    # 帳號
    account = Column(String(50), nullable=False, unique=True)

    # 群組
    group_id = Column(Integer, ForeignKey('groups.id'))

    # 密碼 hash
    _password = Column('password', String(130), nullable=False, default='*', server_default='*')

    # 是否沒換過密碼，沒換過為 0 有換過為 1
    password_status = Column(Integer, nullable=False, default=0, server_default='0')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = self.gen_password_hash(value)

    def gen_password_hash(self, value):
        return sha512_crypt.hash(value)

    def verify_password(self, value):
        return sha512_crypt.verify(value, self._password)


class Group(BaseObject):

    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)

    # 群組名稱
    name = Column(String(100))

    # 類別， 0 為管理者可無視權限設定， 1 為普通使用者會套用權限設定
    type = Column('type', Integer, nullable=False, default=1, server_default='1')

    # self-referential relationship
    ancestor_id = Column(Integer, ForeignKey('groups.id'))
    ancestor = relationship('Group', backref='descendants', remote_side=[id])

    users = relationship('User', backref='group')

    # 最新消息
    news = relationship(News, backref='group')
