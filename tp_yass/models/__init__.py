from pyramid_sqlalchemy import BaseObject

# import or define all models here to ensure they are attached to the
# Base.metadata prior to any initialization routines
from .mymodel import MyModel  # flake8: noqa

