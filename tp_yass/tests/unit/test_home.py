from pyramid import testing

from tp_yass.views.home import home_view

def test_home_view():
    info = home_view(testing.DummyRequest())
    assert info == {'project': 'tp_yass'}
    
