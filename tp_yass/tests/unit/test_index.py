from pyramid import testing

from tp_yass.views.frontend.index import index_view


def test_index_view():
    info = index_view(testing.DummyRequest())
    assert info == {'project': 'tp_yass'}
    
