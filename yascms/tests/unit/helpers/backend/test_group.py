"""因為這是產生樹狀群組邏輯的重要函式，所以雖然沒有讓外部直接呼叫，但還是特別寫了一個測試"""
from yascms.helpers.backend.group import _generate_inheritance_data


def test_generate_inheritance_data_with_group_trees_should_update_group_trees_respectively():
    fake_sub_group_trees = {'type': 2,
                            'inheritance': 2,
                            'descendants': [{'type': 0,
                                             'inheritance': 2,
                                             'descendants': [{'type': 1,
                                                              'inheritance': 2,
                                                              'descendants': []}]}]}
    _generate_inheritance_data(fake_sub_group_trees, 2)
    assert fake_sub_group_trees['descendants'][0]['inheritance'] == 0
    assert fake_sub_group_trees['descendants'][0]['descendants'][0]['inheritance'] == 0

    fake_sub_group_trees = {'type': 2,
                            'inheritance': 2,
                            'descendants': [{'type': 1,
                                             'inheritance': 2,
                                             'descendants': [{'type': 0,
                                                              'inheritance': 2,
                                                              'descendants': []}]}]}
    _generate_inheritance_data(fake_sub_group_trees, 2)
    assert fake_sub_group_trees['descendants'][0]['inheritance'] == 1
    assert fake_sub_group_trees['descendants'][0]['descendants'][0]['inheritance'] == 0
