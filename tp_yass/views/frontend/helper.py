def remove_navbar_root(navbar_trees):
    """前端顯示不需要顯示最上層的 root navbar ，所以拔掉它"""
    navbar_trees = navbar_trees[0]['descendants']
    return navbar_trees
