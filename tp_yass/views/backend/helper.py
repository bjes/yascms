import json
from pathlib import Path
from tempfile import NamedTemporaryFile

import transaction

from tp_yass.dal import DAL
from tp_yass.views.helper.file import get_project_abspath, save_file, convert_image_file


def upload_attachment(cgi_field_storage, upload_sub_dir, prefix, need_resize=False):
    """將上傳的檔案重新亂數命名後存檔

    Args:
        cgi_field_storage: cgi.FieldStorage 物件
        upload_sub_dir: 存放到 uploads/ 目錄下的哪一個子目錄
        prefix: 字串，前綴用
        need_resize: boolean，決定是否要做縮圖處理

    Returns:
        回傳儲存完畢的亂數檔名字串
    """
    upload_file_name = Path(cgi_field_storage.filename)
    destination_dir = get_project_abspath() / 'uploads' / Path(upload_sub_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)  # 若目錄不存在則建立
    if need_resize:
        # 代表這是好站連結的圖片，要轉檔成小尺寸 jpg
        with NamedTemporaryFile(prefix=prefix,
                                suffix=upload_file_name.suffix,
                                delete=False) as tmp_file:
            save_file(cgi_field_storage, tmp_file)
            tmp_file.flush()
            destination_path = destination_dir / f'{tmp_file.name.split("/")[-1].split(".")[0]}.jpg'
            return convert_image_file(tmp_file.name, str(destination_path))
    else:
        # 代表這是一般的附件，不用動內容只有改檔名
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
        upload_sub_dir: 相對於 uploads/ 下的子目錄，檔案會儲存至該處
    """
    attachment_abspath = get_project_abspath() / 'uploads' / Path(upload_sub_dir) / file_name
    if attachment_abspath.is_file():
        attachment_abspath.unlink()


def _recursive_append(group_node, group):
    if group.ancestor_id == group_node['id']:
        group_node['descendants'].append({'id': group.id, 'name': group.name, 'descendants': []})
        return True
    else:
        for descendant_group in group_node['descendants']:
            _recursive_append(descendant_group, group)


def generate_group_trees():
    all_groups = DAL.get_user_group_list()
    group_trees = {}
    for group in all_groups:
        if not group.ancestor_id:
            # 代表是最上層群組
            group_trees = {'id': group.id, 'name': group.name, 'descendants': []}
        else:
            # 代表是第二層以下的群組
            _recursive_append(group_trees, group)
    return group_trees


def import_theme_config(theme_name):
    """匯入上傳上來的佈景主題設定"""
    with transaction.manager, open(get_project_abspath() / 'themes' / theme_name / 'config.json') as f:
        config = json.loads(f.read())
        DAL.save_theme_config(config)
