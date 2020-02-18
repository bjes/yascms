from pyramid_sqlalchemy import BaseObject

from .user import UserModel, GroupModel  # flake8: noqa
from .news import NewsModel, NewsAttachmentModel  # flake8: noqa
from .page import PageModel  # flake8: noqa
from .sys_config import SysConfigModel  # flake8: noqa
from .navbar import NavbarModel # flake8: noqa
from .tag import TagModel # flake8: noqa
