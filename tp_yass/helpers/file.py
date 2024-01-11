from PIL import Image


def convert_image_file(file_path, destination_path) -> bool:
    """將檔案轉檔縮小尺寸後存到指定路徑

    Args:
        file_path: 原始圖檔的路徑
        destination_path: 存放目的路徑含檔名

    Returns:
        轉檔成功回傳檔名
    """
    im = Image.open(file_path)
    if im.mode in ('RGBA', 'P'):
        im = im.convert('RGB')
    new_im = im.resize((120, 60), Image.LANCZOS)
    new_im.save(destination_path, quality=100)
    return destination_path.split('/')[-1]


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
