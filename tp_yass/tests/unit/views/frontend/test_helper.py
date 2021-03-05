from tp_yass.views.frontend.helper import remove_navbar_root


def test_remove_navbar_root_should_remove_root_node():
    return_data = ['foo', 'bar']
    navbar_trees = [{'descendants': return_data}]
    assert remove_navbar_root(navbar_trees) == return_data
