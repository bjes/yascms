from sqlalchemy import (Column,
                        Integer,
                        String,
                        Text,
                        ForeignKey)
from sqlalchemy.orm import relationship

from pyramid_sqlalchemy import BaseObject


class NavbarModel(BaseObject):
    """定義導覽列，其為巢狀架構"""

    __tablename__ = 'navbar'

    # 各導覽列元素的 id，若為 builtin 模組，則統一為 -1 以方便辨識（因為不會存入 db 所以不會有 primary key duplicated 的問題
    id = Column(Integer, primary_key=True)

    # 選單名稱
    name = Column(String(50), nullable=False, server_default='')

    # 無障礙用的名稱，只能是英文。只要不是 leaf node 都要設定此值
    aria_name = Column(String(50), nullable=True)

    # 連結的 url
    url = Column(Text, nullable=False, default='#', server_default='#')

    # 是否為外部連結，若是，點選連結時另開分頁
    is_external = Column(Integer, nullable=False, default=0, server_default='0')

    # 使用的 fontawesome icon
    icon = Column(String(50), nullable=False, default='', server_default='')

    # 選單類型， 1 為選單 （代表其下還有子選單， tree node），2 為連結 （leaf node），3 為分隔線 （dropdown divider)
    # 4 是代表為 builtin news 模組（所以有子選單）， 5 代表 news 模組下的各分類的選單（無子選單），6 代表顯示全部 news 的連結，
    # 7 代表行事曆， 8 代表分機表，9 代表班級網頁，10 代表好站連結
    # 其中 5 和 6 會在 news helper 產生在 4 的下面，資料庫裡面不會有
    type = Column(Integer, nullable=False)

    # 內建的模組才會用到此欄位，用來讓程式判斷這是哪一個模組，以調用該模組的選單產生
    module_name = Column(String(50), nullable=True)

    # 排序
    order = Column(Integer, nullable=False, default=0, server_default='0')

    # 是否顯示，有時候只是想暫時隱藏
    is_visible = Column(Integer, nullable=False, default=1, server_default='1')

    # self-referential relationship
    ancestor_id  = Column(Integer, ForeignKey('navbar.id'))
    ancestor = relationship('NavbarModel', backref='descendants', remote_side=[id])

