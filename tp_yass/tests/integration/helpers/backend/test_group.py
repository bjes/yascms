from tp_yass.helpers.backend import group


def test_generate_group_trees_should_return_group_trees(init_db_session):
    group_trees = group.generate_group_trees()
    assert isinstance(group_trees, dict)
    for key in ('id', 'name', 'type', 'inheritance', 'descendants'):
        assert key in group_trees
