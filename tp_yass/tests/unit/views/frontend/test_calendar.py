from pyramid.testing import DummyRequest

from tp_yass.views.frontend import calendar


def test_calendar_view_should_return_list(mocker):
    mocker.patch.object(calendar, "generate_navbar_trees")
    response = calendar.calendar_view(DummyRequest())
    assert isinstance(response, dict)
    valid_keys = ['navbar_trees', 'NavbarType']
    for key in valid_keys:
        assert key in response
