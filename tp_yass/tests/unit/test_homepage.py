from pyramid import testing

from tp_yass.views.frontend.homepage import homepage_view


def test_homepage_view():
    info = homepage_view(testing.DummyRequest())
    assert info == {'project': 'tp_yass'}

