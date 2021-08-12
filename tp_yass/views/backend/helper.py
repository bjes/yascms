import json
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

import transaction

from tp_yass.dal import DAL
from tp_yass.views.helper.file import get_project_abspath, save_file, convert_image_file
from tp_yass.enum import GroupType


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


def _generate_inheritance_data(sub_group_trees, inherited_permission):
    """上層 node 的權限會繼承至下層的 node，權限高低依序是 ADMIN > STAFF > NORMAL

    Args:
        sub_group_trees: 由 generate_group_trees() 產生的 group_trees 移掉最上層的 json 資料結構，移掉一層才好用遞迴處理
        inherited_permission: 目前所繼承的權限
    """
    if sub_group_trees['type'] <= inherited_permission:
        sub_group_trees['inheritance'] = sub_group_trees['type']
    else:
        sub_group_trees['inheritance'] = inherited_permission

    for each_group in sub_group_trees['descendants']:
        if each_group['descendants']:
            _generate_inheritance_data(each_group, sub_group_trees['inheritance'])
        else:
            if each_group['type'] <= sub_group_trees['inheritance']:
                each_group['inheritance'] = each_group['type']
            else:
                each_group['inheritance'] = sub_group_trees['inheritance']


def _recursive_append(group_node, group):
    if group.ancestor_id == group_node['id']:
        descendant = {'id': group.id,
                      'name': group.name,
                      'type': group.type,
                      'inheritance': GroupType.NORMAL.value,  # 預設是普通權限
                      'descendants': []}
        group_node['descendants'].append(descendant)
        return True
    else:
        for descendant_group in group_node['descendants']:
            _recursive_append(descendant_group, group)


def generate_group_trees():
    """產生前端需要的 group trees json 資料結構"""
    all_groups = DAL.get_group_list()
    group_trees = {}
    for group in all_groups:
        if not group.ancestor_id:
            # 代表是最上層群組，最上層群組是根群組，預設的繼承權限為 GroupType.NORMAL
            group_trees = {'id': group.id,
                           'name': group.name,
                           'type': group.type,
                           'inheritance': GroupType.NORMAL.value,
                           'descendants': []}
        else:
            # 代表是第二層以下的群組
            _recursive_append(group_trees, group)
    _generate_inheritance_data(group_trees, GroupType.NORMAL.value)
    return group_trees


class ThemeImporter:
    """用來處理匯入樣板"""

    def __init__(self, theme_name, base_dir=None):
        """初始化

        Args:
            theme_name: 樣板名稱
            base_dir: 作為 root dir 的起點，為 pathlib.PosixPath 的實體。若沒有指定則會使用 tp_yass 專案的 base dir
        """
        self.theme_name = theme_name
        if base_dir is None:
            self.base_dir = get_project_abspath()
        else:
            self.base_dir = base_dir
        self.default_dest = self.base_dir / 'uploads/themes' / self.theme_name / 'banners'

    def import_theme(self):
        self._import_theme_config()
        self.import_theme_banners()

    def import_theme_banners(self, src=None, dest=None):
        """匯入指定的佈景主題橫幅檔案"""
        if src is None:
            src = self.base_dir / 'themes' / self.theme_name / 'static/img/banners'
        if dest is None:
            dest = self.default_dest
        dest.mkdir(parents=True, exist_ok=True)
        for banner in src.glob('*'):
            shutil.copy(banner, dest)

    def _import_theme_config(self):
        """匯入指定的佈景主題設定檔"""
        with transaction.manager, open(self.base_dir / 'themes' / self.theme_name / 'config.json') as f:
            config = json.loads(f.read())
            DAL.add_theme_config(config)
