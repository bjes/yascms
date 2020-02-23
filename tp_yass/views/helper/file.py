from pathlib import Path

import tp_yass


def save_file(cgi_field_storage, file_obj, bulk_size=5120000) -> bool:
    """將檔案儲存到指定路徑

    Args:
        cgi_field_storage: cgi.FieldStorage 物件
        file_obj: 存放目的地檔案物件
        bulk_size: 每次讀取的大小，避免一次讀進來記憶體爆炸。預設一次讀 5 MB

    Returns:
        object: Path
        上傳成功回傳 True
    """
    while True:
        tmp_store = cgi_field_storage.file.read(bulk_size)
        if tmp_store:
            file_obj.write(tmp_store)
        else:
            break
    return True


def get_static_abspath() -> Path:
    """回傳 static 目錄的絕對路徑

    Returns:
        object: Path
        pathlib.Path 物件
    """
    return get_project_abspath() / 'themes' / 'default' / 'static'


def get_project_abspath() -> Path:
    """回傳 tp_yass 專案的絕對路徑

    Returns:
        object: Path
        pathlib.Path 物件
    """
    return Path(tp_yass.__file__).parent
