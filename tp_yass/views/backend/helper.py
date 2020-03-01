from pathlib import Path
from tempfile import NamedTemporaryFile

from tp_yass.views.helper.file import get_static_abspath, save_file


def upload_attachment(cgi_field_storage, upload_sub_dir, prefix):
    """將上傳的檔案重新亂數命名後存檔

    Args:
        cgi_field_storage: cgi.FieldStorage 物件
        upload_sub_dir: 存放到 static/uploads/ 目錄下的哪一個子目錄
        prefix: 字串，前綴用

    Returns:
        回傳儲存完畢的亂數檔名字串
    """
    upload_file_name = Path(cgi_field_storage.filename)
    destination_dir = get_static_abspath() / 'uploads' / Path(upload_sub_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)  # 若目錄不存在則建立
    with NamedTemporaryFile(dir=str(destination_dir),
                            prefix=prefix,
                            suffix=upload_file_name.suffix,
                            delete=False) as destination_file:
        save_file(cgi_field_storage, destination_file)
        return str(Path(destination_file.name).name)


def delete_attachment(file_name, upload_sub_dir):
    """移除指定的上傳附件實體檔案

    Args:
        file_name: 儲存在磁碟上的檔名
        upload_sub_dir: 相對於 static 下的子目錄，檔案會儲存至該處
    """
    attachment_abspath = get_static_abspath() / 'uploads' / Path(upload_sub_dir) / file_name
    attachment_abspath.unlink()
