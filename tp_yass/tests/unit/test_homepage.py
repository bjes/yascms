from pyramid import testing

from tp_yass.views.frontend import homepage


def test_homepage_view(mocker):
    request = testing.DummyRequest()
    request.site_config = {'site_homepage_news_quantity': 10}
    mocker.patch.object(homepage, 'DAL')
    mocker.patch.object(homepage, 'remove_navbar_root')
    mocker.patch.object(homepage, 'generate_navbar_trees')
    info = homepage.homepage_view(request)
    for key in ['NavbarType', 'link_list', 'navbar_trees', 'news_list', 'telext_list']:
        assert key in info

