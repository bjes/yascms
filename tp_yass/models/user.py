from passlib.hash import sha512_crypt
from sqlalchemy import (Column,
                        Integer,
                        String,
                        Text)
from pyramid_sqlalchemy import BaseObject


class User(BaseObject):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    account = Column(String(50), nullable=False, unique=True)
    _password = Column('password', String(130), nullable=False, default='*')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = self.gen_password_hash(value)

    def gen_password_hash(self, value):
        '''產生密碼 hash'''
        return sha512_crypt.hash(value)

    def verify_password(self, value):
        '''驗證密碼是否正確'''
        return sha512_crypt.verify(value, self._password)
