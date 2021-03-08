import pytest
from pyramid.testing import DummyRequest

from tp_yass.views.helper.navbar import generate_navbar_trees, news_factory


def test_generate_navbar_trees_with_params_should_return_navbar_trees_list(pyramid_config, transaction):
    navbar_trees = generate_navbar_trees(DummyRequest())
    assert isinstance(navbar_trees, list)
    assert len(navbar_trees) == 1
    assert isinstance(navbar_trees[0], dict)
    valid_keys = ['id', 'name', 'aria_name', 'url', 'is_external', 'icon', 'type', 'module_name', 'order', 'descendants']
    for key in navbar_trees[0].keys():
        assert key in valid_keys
    assert True


def test_news_factory_should_return_news_sub_navbars(transaction):
    news_sub_navbars = news_factory()
    assert isinstance(news_sub_navbars, list)
    valid_keys = ['id', 'type', 'category_id', 'name', 'url']
    for sub_navbar in news_sub_navbars:
        assert isinstance(sub_navbar, dict)
        for key in sub_navbar.keys():
            assert key in valid_keys
    assert True
