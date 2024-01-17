from pathlib import Path

from yascms.helpers.backend import file
from yascms import helpers


def mock_get_project_abspath(mocker, datadir):
    fake_get_project_abspath_func = mocker.MagicMock()
    fake_get_project_abspath_func.return_value = datadir
    mocker.patch.object(file, 'get_project_abspath', fake_get_project_abspath_func)


def test_upload_attachment_should_save_file_and_return_file_name(mocker, datadir):
    upload_file_name_suffix = 'jpg'
    upload_file_name = f'original_upload_file_name.{upload_file_name_suffix}'
    dest_file_name_base = 'random'
    mock_cgi_field_storage = mocker.Mock()
    mock_cgi_field_storage.filename = upload_file_name
    upload_sub_dir = 'foo'
    prefix = 'bar'

    mock_get_project_abspath(mocker, datadir)

    mocker.patch('yascms.helpers.backend.file.NamedTemporaryFile').return_value.__enter__.return_value.name = f'/tmp/what/ever/{dest_file_name_base}.{upload_file_name_suffix}'
    mocker.patch.object(file, 'save_file')

    # 驗證傳入 need_resize 做縮圖處理的流程
    mocker.patch.object(file, 'convert_image_file')
    file.upload_attachment(mock_cgi_field_storage, upload_sub_dir, prefix, need_resize=True)
    file.convert_image_file.assert_called_once()

    # 驗證 need_resize 為 False 的流程
    result = file.upload_attachment(mock_cgi_field_storage, upload_sub_dir, prefix)
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

    file.delete_attachment(test_file_name, test_sub_dir)
    assert not target_file.exists()
