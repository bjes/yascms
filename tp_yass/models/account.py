from passlib.hash import sha256_crypt
from sqlalchemy import (Column,
                        Integer,
                        String,
                        ForeignKey)
from sqlalchemy.orm import relationship
from pyramid_sqlalchemy import BaseObject

from tp_yass import models
from tp_yass.models.associations import users_groups_association, groups_pages_association
from tp_yass.enum import GroupType


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
                          secondary=users_groups_association,
                          order_by='GroupModel.id',
                          back_populates='users')

    # 關聯的 auth logs
    auth_logs = relationship('models.auth_log.AuthLogModel', backref='user')

    # 密碼 hash
    _password = Column('password', String(77), nullable=False, default='*', server_default='*')

    # 0 還沒改密碼， 1 正常狀態， 2 被停用
    status = Column(Integer, nullable=False, default=0, server_default='0')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = self.gen_password_hash(value)

    def gen_password_hash(self, value):
        return sha256_crypt.hash(value)

    def verify_password(self, value):
        return sha256_crypt.verify(value, self._password)


class GroupModel(BaseObject):

    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)

    # 群組名稱
    name = Column(String(100), nullable=False)

    # 類別，定義請參照 tp_yass.enum.GroupType
    type = Column('type', Integer, nullable=False, default=GroupType.STAFF.value,
                  server_default=str(GroupType.STAFF.value))

    # 排序的依據，數字愈小排越前面
    order = Column(Integer, nullable=False, default=0, server_default='0')

    # self-referential relationship
    ancestor_id = Column(Integer, ForeignKey('groups.id'))
    ancestor = relationship('GroupModel', backref='descendants', remote_side=[id])

    users = relationship('UserModel',
                         secondary=users_groups_association,
                         back_populates='groups')

    # 最新消息
    news = relationship('models.news.NewsModel', backref='group')

    # 這個群組有編輯權限的單一頁面
    pages = relationship('models.page.PageModel', secondary=groups_pages_association, back_populates='groups')

    # 這個群組上傳的好站連結
    links = relationship('models.link.LinkModel', backref='group')
