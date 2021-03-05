from pyramid.testing import DummyRequest

from tp_yass.views.backend import homepage


def test_homepage_view_should_return_list():
    assert homepage.backend_homepage_view(DummyRequest()) == {}
