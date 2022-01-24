import json
import shutil

import transaction

from tp_yass.dal import DAL
from tp_yass.helpers import get_project_abspath


class ThemeController:
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
        self.uploaded_banners_dir = self.base_dir / 'uploads/themes' / self.theme_name / 'banners'
        self.static_symlink = self.base_dir / f'static/{self.theme_name}'

    def import_theme(self):
        """匯入樣板"""
        self._import_theme_config()
        self.import_theme_banners()
        self._setup_static_assets()

    def delete_theme(self):
        if self.static_symlink.exists():
            self.static_symlink.unlink()
        if self.uploaded_banners_dir.parent.exists():
            shutil.rmtree(self.uploaded_banners_dir.parent)
        theme_dir = self.base_dir / 'themes' / self.theme_name
        if theme_dir.exists():
            shutil.rmtree(theme_dir)
        with transaction.manager:
            DAL.delete_theme_config(self.theme_name)


    def import_theme_banners(self, src=None, dest=None):
        """匯入指定的佈景主題橫幅檔案"""
        if src is None:
            src = self.base_dir / 'themes' / self.theme_name / 'static/img/banners'
        if dest is None:
            dest = self.uploaded_banners_dir
        dest.mkdir(parents=True, exist_ok=True)
        for banner in src.glob('*'):
            shutil.copy(banner, dest)

    def _import_theme_config(self):
        """匯入指定的佈景主題設定檔"""
        with transaction.manager, open(self.base_dir / 'themes' / self.theme_name / 'config.json') as f:
            config = json.loads(f.read())
            DAL.add_theme_config(config)

    def _setup_static_assets(self):
        """在 tp_yass/static 目錄下建立 soft link 至 themes 對應樣板下的 static 目錄"""
        dest = f'../themes/{self.theme_name}/static'
        if self.static_symlink.exists():
            self.static_symlink.unlink()
        self.static_symlink.symlink_to(dest)
