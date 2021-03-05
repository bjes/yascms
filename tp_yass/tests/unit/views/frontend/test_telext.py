from pyramid.testing import DummyRequest

from tp_yass.views.frontend import telext


def test_telext_view_should_return_telext_list(mocker):
    mocker.patch.object(telext.DAL, "get_pinned_telext_list")
    mocker.patch.object(telext, 'generate_navbar_trees')
    mocker.patch.object(telext, 'remove_navbar_root')

    response = telext.telext_view(DummyRequest())
    assert isinstance(response, dict)
    valid_keys = ['navbar_trees', 'NavbarType', 'telext_list']
    for key in valid_keys:
        assert key in response
