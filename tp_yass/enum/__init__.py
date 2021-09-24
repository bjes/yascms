import enum
from enum import IntEnum


class NavbarType(IntEnum):
    """用來表示 navbar 的類型"""

    # 1 為選單 （代表其下還有子選單， tree node）
    TREE_NODE = 1

    # 2 為連結 （leaf node，一種是直接輸入 url，一種是連結單一頁面）
    LEAF_NODE = 2

    # 3 為分隔線 （dropdown divider)
    DROPDOWN_DIVIDER = 3

    # 4 是代表為 builtin news 模組（所以有子選單）
    BUILTIN_NEWS = 4

    # 5 代表 news 模組下的各分類的選單（無子選單），此類別會在 _news_factory() 產生在 4 的下面，資料庫裡面不會有
    BUILTIN_NEWS_SUBTYPE = 5

    # 6 代表顯示全部 news 的連結，此類別會在 _news_factory() 產生在 4 的下面，資料庫裡面不會有
    BUILTIN_NEWS_ALL = 6

    # 7 代表分機表
    BUILTIN_TELEXT = 7

    # 8 代表好站連結
    BUILTIN_LINKS = 8


class AuthLogType(IntEnum):
    """用來表示 auth log 的類型"""

    # 1 代表登入
    LOGIN = 1

    # 2 代表登出
    LOGOUT = 2

    # 代表密碼輸入錯誤
    WRONG_PASSWORD = 3


class GroupType(IntEnum):
    """用來表示群組的類型"""

    # 0 為管理群組權限可無視權限設定
    ADMIN = 0

    # 1 為行政群組權限（可張貼最新消息）
    STAFF = 1

    # 3 為一般群組權限（比方教師）
    NORMAL = 2


class ThemeConfigCustomType(enum.IntEnum):
    """用來表示樣板自訂設定的每個設定的類型"""

    # 字串
    STRING = 1

    # 布林值
    BOOLEAN = 2

    # 整數
    INTEGER = 3


class HomepageItemType(enum.IntEnum):
    """用來表示首頁顯示順序的類別"""

    # 最新消息模組
    NEWS = 1

    # 單一頁面模組
    PAGE = 2

    # 分機表模組
    TELEXT = 3

    # 好站連結模組
    LINKS = 4


class HomepageItemParamsSubType(enum.IntEnum):
    """用來定義 sub type，會用到 sub type 的為最新消息與好站連結"""

    # 未指定
    UNSPECIFIED = 0
