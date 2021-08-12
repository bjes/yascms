from pathlib import Path

from tp_yass.views.backend import helper


def mock_get_project_abspath(mocker, datadir):
    fake_get_project_abspath_func = mocker.MagicMock()
    fake_get_project_abspath_func.return_value = datadir
    mocker.patch.object(helper, 'get_project_abspath', fake_get_project_abspath_func)


def test_upload_attachment_should_save_file_and_return_file_name(mocker, datadir):
    upload_file_name_suffix = 'jpg'
    upload_file_name = f'original_upload_file_name.{upload_file_name_suffix}'
    dest_file_name_base = 'random'
    mock_cgi_field_storage = mocker.Mock()
    mock_cgi_field_storage.filename = upload_file_name
    upload_sub_dir = 'foo'
    prefix = 'bar'

    mock_get_project_abspath(mocker, datadir)

    mocker.patch('tp_yass.views.backend.helper.NamedTemporaryFile').return_value.__enter__.return_value.name = f'/tmp/what/ever/{dest_file_name_base}.{upload_file_name_suffix}'
    mocker.patch.object(helper, 'save_file')

    # 驗證傳入 need_resize 做縮圖處理的流程
    mocker.patch.object(helper, 'convert_image_file')
    helper.upload_attachment(mock_cgi_field_storage, upload_sub_dir, prefix, need_resize=True)
    helper.convert_image_file.assert_called_once()

    # 驗證 need_resize 為 False 的流程
    result = helper.upload_attachment(mock_cgi_field_storage, upload_sub_dir, prefix)
    assert result == f'{dest_file_name_base}.{upload_file_name_suffix}'



def test_delete_attachment_should_delete_file(mocker, datadir):
    mock_get_project_abspath(mocker, datadir)

    # 先把要用來測試刪除的測試檔案建立好
    test_file_name = 'bar'
    test_sub_dir = 'foo'
    target_dir = Path(datadir, 'uploads', test_sub_dir)
    target_dir.mkdir(parents=True)
    target_file = target_dir / test_file_name
    target_file.touch()
    assert target_file.exists()

    helper.delete_attachment(test_file_name, test_sub_dir)
    assert not target_file.exists()


def test_theme_importer_should_work_as_expected(mocker):
    mocker.patch.object(helper.DAL, 'add_theme_config')
    mocker.patch.object(helper.shutil, 'copy')
    theme_importer = helper.ThemeImporter('tp_yass2020')
    theme_importer.import_theme()  # 專案預設的佈景主題就是 tp_yass2020 一定存在
    helper.DAL.add_theme_config.assert_called_once()
    helper.shutil.copy.assert_called()


def test_generate_inheritance_data_with_group_trees_should_update_group_trees_respectively():
    fake_sub_group_trees = {'type': 2,
                            'inheritance': 2,
                            'descendants': [{'type': 0,
                                             'inheritance': 2,
                                             'descendants': [{'type': 1,
                                                              'inheritance': 2,
                                                              'descendants': []}]}]}
    helper._generate_inheritance_data(fake_sub_group_trees, 2)
    assert fake_sub_group_trees['descendants'][0]['inheritance'] == 0
    assert fake_sub_group_trees['descendants'][0]['descendants'][0]['inheritance'] == 0

    fake_sub_group_trees = {'type': 2,
                            'inheritance': 2,
                            'descendants': [{'type': 1,
                                             'inheritance': 2,
                                             'descendants': [{'type': 0,
                                                              'inheritance': 2,
                                                              'descendants': []}]}]}
    helper._generate_inheritance_data(fake_sub_group_trees, 2)
    assert fake_sub_group_trees['descendants'][0]['inheritance'] == 1
    assert fake_sub_group_trees['descendants'][0]['descendants'][0]['inheritance'] == 0
