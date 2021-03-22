from pyramid.testing import DummyRequest

from tp_yass.views.frontend import link


def test_links_view_should_return_dict(mocker):
    mocker.patch.object(link, 'generate_navbar_trees')
    mocker.patch.object(link.DAL, 'get_link_category_list')
    response = link.links_view(DummyRequest())
    assert isinstance(response, dict)
    valid_keys = ['navbar_trees', 'NavbarType', 'link_category_list']
    for key in valid_keys:
        assert key in response
