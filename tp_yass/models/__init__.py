from pyramid_sqlalchemy import BaseObject

from .user import UserModel, GroupModel  # flake8: noqa
from .news import NewsModel, NewsAttachmentModel  # flake8: noqa
from .syssettings import SysSettingsModel  # flake8: noqa
