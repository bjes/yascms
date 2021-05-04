from pathlib import Path

from tp_yass.views.backend import helper


def test_generate_group_trees_should_return_group_trees(init_db_session):
    group_trees = helper.generate_group_trees()
    assert isinstance(group_trees, dict)
    for key in ('id', 'name', 'type', 'inheritance', 'descendants'):
        assert key in group_trees

