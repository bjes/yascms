from passlib.hash import sha512_crypt
from sqlalchemy import (Table,
                        Column,
                        Integer,
                        String,
                        ForeignKey)
from sqlalchemy.orm import relationship
from pyramid_sqlalchemy import BaseObject

from .news import NewsModel


association_table = Table('users_groups_association',
                          BaseObject.metadata,
                          Column('users_id', Integer, ForeignKey('users.id')),
                          Column('groups_id', Integer, ForeignKey('groups.id')))


class UserModel(BaseObject):

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

    groups = relationship('GroupModel',
                          secondary=association_table,
                          back_populates='users')

    # 密碼 hash
    _password = Column('password', String(130), nullable=False, default='*', server_default='*')

    # 0 還沒改密碼， 1 正常狀態， 2 被鎖定
    status = Column(Integer, nullable=False, default=0, server_default='0')

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


class GroupModel(BaseObject):

    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)

    # 群組名稱
    name = Column(String(100))

    # 類別， 0 為管理者可無視權限設定， 1 為普通使用者會套用權限設定
    type = Column('type', Integer, nullable=False, default=1, server_default='1')

    # 排序的依據，數字愈小排越前面
    order = Column(Integer, nullable=False, default=0, server_default='0')

    # self-referential relationship
    ancestor_id = Column(Integer, ForeignKey('groups.id'))
    ancestor = relationship('GroupModel', backref='descendants', remote_side=[id])

    users = relationship('UserModel',
                         secondary=association_table,
                         back_populates='groups')

    # 最新消息
    news = relationship(NewsModel, backref='group')
