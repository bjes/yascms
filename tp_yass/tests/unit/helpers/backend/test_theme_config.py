from tp_yass.helpers.backend.theme_config import ThemeImporter


def test_theme_importer_import_theme_should_work_as_expected(mocker):
    """ backend 的 theme_config 已經有實際跑 integration test 確認資料庫與 banners 都正常出現，
    所以這邊只跑 mock 驗證"""

    mocker.patch.object(ThemeImporter, '_import_theme_config')
    mocker.patch.object(ThemeImporter, 'import_theme_banners')

    theme_importer = ThemeImporter('tp_yass2020')
    theme_importer.import_theme()

    theme_importer._import_theme_config.assert_called_once()
    theme_importer.import_theme_banners.assert_called_once()
