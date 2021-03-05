from tp_yass.helper import sanitize_input

def test_sanitize_input_with_param_should_sanitize_and_return():
    assert sanitize_input(10, int, 20) == 10
    assert sanitize_input('10', int, 20) == 10
    assert sanitize_input('xxx', int, 20) == 20

    assert sanitize_input('foo', str, 'oops') == 'foo'
    assert sanitize_input(20, str, 'oops') == '20'
