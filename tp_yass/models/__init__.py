from pyramid_sqlalchemy import BaseObject

from .user import UserModel, GroupModel  # flake8: noqa
from .news import NewsModel, NewsAttachmentModel  # flake8: noqa
from .page import PageModel, PageAttachmentModel  # flake8: noqa
from .link import LinkModel, LinkCategoryModel  # flake8: noqa
from .site_config import SiteConfigModel  # flake8: noqa
from .navbar import NavbarModel  # flake8: noqa
from .tag import TagModel  # flake8: noqa
from .telext import TelExtModel  # flake8: noqa
