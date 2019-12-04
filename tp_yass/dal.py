import logging

from pyramid_sqlalchemy import Session as DBSession

from tp_yass.models.user import UserModel


class DAL:

    @staticmethod
    def get_user(account, password):
        user = DBSession.query(UserModel).filter_by(account=account).one_or_none()
        if user and user.verify_password(password):
            return user
