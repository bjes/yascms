import pytest
from pyramid.testing import DummyRequest

from tp_yass.views.helper.navbar import generate_navbar_trees, news_factory


def test_generate_navbar_trees_with_params_should_return_navbar_trees_list(pyramid_config, init_db_session):
    navbar_trees = generate_navbar_trees(DummyRequest())
    assert isinstance(navbar_trees, dict)
    # 檢驗 root 選單
    valid_keys = ['id', 'name', 'aria_name', 'type', 'module_name', 'descendants']
    for key in navbar_trees.keys():
        assert key in valid_keys

    # 檢驗第二層選單 (懶得跑迴圈了，檢查到第二層就好)
    valid_keys = ['id', 'name', 'aria_name', 'url', 'is_href_blank', 'icon', 'type', 'module_name', 'order', 'descendants']
    for sub_navbar in navbar_trees['descendants']:
        for key in sub_navbar.keys():
            assert key in valid_keys


def test_news_factory_should_return_news_sub_navbars(init_db_session):
    news_sub_navbars = news_factory()
    assert isinstance(news_sub_navbars, list)
    valid_keys = ['id', 'type', 'category_id', 'name', 'url']
    for sub_navbar in news_sub_navbars:
        assert isinstance(sub_navbar, dict)
        for key in sub_navbar.keys():
            assert key in valid_keys
    assert True
