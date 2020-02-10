import logging


logger = logging.getLogger(__name__)


def group_finder(user_name, request):
    '''根據 session 存放的 group 資訊，找到登入的使用者所屬的 group id 列表'''

    groups = request.session.get('groups', None)
    if groups:
        # groups 為一個多個 dict 組成的二維陣列，其中 key id 儲存了每個 group 的 id
        # group name 可能會改，但 id 不會改，所以用 id 作為判斷依據
        group_list = list({i['id'] for each_group_list in groups for i in each_group_list})
        logger.debug('使用者 %s 透過 group_finder 取得群組列表為 %s', request.session['account'], group_list)
        return group_list
