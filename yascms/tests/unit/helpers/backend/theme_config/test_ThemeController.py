import pathlib

from yascms.helpers.backend.theme_config import ThemeController


def test_import_theme_should_work_as_expected(mocker):
    """ backend 的 theme_config 已經有實際跑 integration test 確認資料庫與 banners 都正常出現，
    所以這邊只跑 mock 驗證"""

    mocker.patch.object(ThemeController, '_import_theme_config')
    mocker.patch.object(ThemeController, 'import_theme_banners')
    mocker.patch.object(ThemeController, '_setup_static_assets')

    theme_importer = ThemeController('yascms2020')
    theme_importer.import_theme()

    theme_importer._import_theme_config.assert_called_once()
    theme_importer.import_theme_banners.assert_called_once()
    theme_importer._setup_static_assets.assert_called_once()


def test__setup_static_assets_should_link_to_theme_static_path(tmp_path):
    """雖然沒有讓外部呼叫，但要確保 _setup_static_assets() 有建立 soft link 所以還是對 private method 寫測試"""
    theme_name = 'yascms2020'
    pathlib.Path(tmp_path / 'static').mkdir(parents=True)
    pathlib.Path(tmp_path / f'themes/{theme_name}/static').mkdir(parents=True)

    theme_importer = ThemeController(theme_name, tmp_path)
    theme_importer._setup_static_assets()
    assert (tmp_path / f'static/{theme_name}').resolve() == tmp_path / f'themes/{theme_name}/static'
