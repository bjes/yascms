import io

from tp_yass.helpers.file import save_file, convert_image_file


def test_save_file_with_cgi_field_storage_and_file_obj_should_copy_contents(mocker):
    content = 'foo'
    mock_field_storage = mocker.Mock()
    mock_field_storage.file = io.StringIO(content)
    file_obj = io.StringIO()
    assert save_file(mock_field_storage, file_obj)
    file_obj.seek(0)
    assert file_obj.read() == content


def test_convert_image_file_should_convert_image_successfully(datadir, tmp_path):
    original_img_name = 'logo.png'
    new_img_name = 'new_logo.png'
    destination_path = tmp_path / new_img_name
    assert convert_image_file(str(datadir / original_img_name), str(destination_path)) == new_img_name
    assert destination_path.exists()

