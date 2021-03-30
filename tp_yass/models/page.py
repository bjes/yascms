from pyramid_sqlalchemy import BaseObject
from sqlalchemy import (Column,
                        String,
                        Integer,
                        Text,
                        ForeignKey,
                        Table)
from sqlalchemy.orm import relationship

from tp_yass import models
from tp_yass.models.associations import pages_tags_association, groups_pages_association


class PageAttachmentModel(BaseObject):
    """page 的上傳附檔"""

    __tablename__ = 'page_attachments'

    id = Column(Integer, primary_key=True)

    # 上傳時原本的檔案名稱
    original_name = Column(String(100), nullable=False)

    # 儲存至硬碟上的檔案名稱
    real_name = Column(String(100), nullable=False)

    page_id = Column(Integer, ForeignKey('pages.id'))


class PageModel(BaseObject):
    """單頁網頁"""

    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True)

    # 標題
    title = Column(String(100), nullable=False)

    # 內容
    content = Column(Text, nullable=False, default='')

    # 上傳附件
    attachments = relationship('PageAttachmentModel', backref='page', cascade='all, delete-orphan')

    # 標籤
    tags = relationship('models.tag.TagModel', secondary=pages_tags_association, back_populates='pages')

    # 擁有這個頁面編輯權限的群組
    groups = relationship('models.user.GroupModel', secondary=groups_pages_association, back_populates='pages')

    navbar = relationship('models.navbar.NavbarModel', uselist=False, back_populates='page')
