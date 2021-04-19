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

    # 5 代表 news 模組下的各分類的選單（無子選單），此類別會在 news_factory() 產生在 4 的下面，資料庫裡面不會有
    BUILTIN_NEWS_SUBTYPE = 5

    # 6 代表顯示全部 news 的連結，此類別會在 news_factory() 產生在 4 的下面，資料庫裡面不會有
    BUILTIN_NEWS_ALL = 6

    # 7 代表行事曆
    BUILTIN_CALENDAR = 7

    # 8 代表分機表
    BUILTIN_TELEXT = 8

    # 9 代表好站連結
    BUILTIN_LINKS = 9


class AuthLogType(IntEnum):
    """用來表示 auth log 的類型"""

    # 1 代表登入
    LOGIN = 1

    # 2 代表登出
    LOGOUT = 2

    # 代表密碼輸入錯誤
    WRONG_PASSWORD = 3
