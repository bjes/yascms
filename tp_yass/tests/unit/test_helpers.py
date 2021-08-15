from pathlib import Path

import tp_yass
from tp_yass.helpers import sanitize_input, get_project_abspath


def test_sanitize_input_with_param_should_sanitize_and_return():
    assert sanitize_input(10, int, 20) == 10
    assert sanitize_input('10', int, 20) == 10
    assert sanitize_input('xxx', int, 20) == 20

    assert sanitize_input('foo', str, 'oops') == 'foo'
    assert sanitize_input(20, str, 'oops') == '20'


def test_get_project_abspath_should_return_project_abspath():
    assert get_project_abspath() == Path(tp_yass.__file__).parent
