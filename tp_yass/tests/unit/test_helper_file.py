import io
import pathlib

import tp_yass
from tp_yass.views.helper.file import get_project_abspath, save_file


def test_save_file_with_cgi_field_storage_and_file_obj_should_copy_contents(mocker):
    content = 'foo'
    mock_field_storage = mocker.Mock()
    mock_field_storage.file = io.StringIO(content)
    file_obj = io.StringIO()
    assert save_file(mock_field_storage, file_obj)
    file_obj.seek(0)
    assert file_obj.read() == content


def test_get_project_abspath_should_return_project_abspath():
    assert get_project_abspath() == pathlib.Path(tp_yass.__file__).parent
