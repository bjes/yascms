def group_finder(user_name, request):
    '''根據 session 存放的 group 資訊，找到登入的使用者所屬的 group id 列表'''

    groups = request.session.get('groups', None)
    if groups:
        # groups 為一個多個 dict 組成的二維陣列，其中 key id 儲存了每個 group 的 id
        # group name 可能會改，但 id 不會改，所以用 id 作為判斷依據
        return [ i['id'] for each_group_list in groups for i in each_group_list ]
    else:
        return None
