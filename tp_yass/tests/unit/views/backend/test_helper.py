from pathlib import Path

from tp_yass.views.backend import helper
from tp_yass.models.user import GroupModel


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



def test_generate_group_trees_should_return_group_trees(mocker):
    root_group = GroupModel(id=1, name='濱江國小')
    academic_affairs_office_group = GroupModel(id=2, name='教務處', ancestor_id=1)
    student_affairs_office_group = GroupModel(id=3, name='學務處', ancestor_id=1)
    information_management_section_group = GroupModel(id=4, name='資訊組', ancestor_id=2)
    student_activities_section_group = GroupModel(id=5, name='訓育組', ancestor_id=3)

    # 同父群組的要排在一起，這是 DAL.get_user_group_list() 的行為
    fake_group_list = [root_group, academic_affairs_office_group, student_affairs_office_group,
                       information_management_section_group, student_activities_section_group]

    mocker.patch.object(helper.DAL, 'get_user_group_list', return_value=fake_group_list)


def test_import_theme_config_should_call_dal_save_theme_config_once(mocker):
    mocker.patch.object(helper.DAL, 'save_theme_config')
    helper.import_theme('tp_yass2020') # 專案預設的佈景主題就是 tp_yass2020 一定存在
    helper.DAL.save_theme_config.assert_called_once()
