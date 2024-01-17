from pyramid.testing import DummyRequest

from yascms.helpers.navbar import generate_navbar_trees


def test_generate_navbar_trees_with_params_should_return_navbar_trees_list(pyramid_config, init_db_session):
    navbar_trees = generate_navbar_trees(DummyRequest())
    assert isinstance(navbar_trees, dict)
    # 檢驗 root 選單
    valid_keys = ['id', 'name', 'email', 'aria_name', 'type', 'module_name', 'descendants']
    for key in navbar_trees.keys():
        assert key in valid_keys

    # 檢驗第二層選單 (懶得跑迴圈了，檢查到第二層就好)
    valid_keys = ['id', 'name', 'email', 'aria_name', 'url', 'is_href_blank', 'icon', 'type',
                  'module_name', 'order', 'descendants']
    for sub_navbar in navbar_trees['descendants']:
        for key in sub_navbar.keys():
            assert key in valid_keys
