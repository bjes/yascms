from sqlalchemy import (Table,
                        Column,
                        Integer,
                        ForeignKey)
from pyramid_sqlalchemy import BaseObject


users_groups_association = Table('users_groups_association',
                                 BaseObject.metadata,
                                 Column('user_id', Integer, ForeignKey('users.id')),
                                 Column('group_id', Integer, ForeignKey('groups.id')))


groups_pages_association = Table('groups_pages_association',
                                 BaseObject.metadata,
                                 Column('group_id', Integer, ForeignKey('groups.id')),
                                 Column('page_id', Integer, ForeignKey('pages.id')))


news_tags_association = Table('news_tags_association',
                              BaseObject.metadata,
                              Column('news_id', Integer, ForeignKey('news.id')),
                              Column('tag_id', Integer, ForeignKey('tags.id')))


pages_tags_association = Table('pages_tags_association',
                               BaseObject.metadata,
                               Column('page_id', Integer, ForeignKey('pages.id')),
                               Column('tag_id', Integer, ForeignKey('tags.id')))
