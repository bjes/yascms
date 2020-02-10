import logging


logger = logging.getLogger(__name__)


def group_finder(user_name, request):
    """回傳 session 存放的 group_id_list"""

    group_id_list = request.session.get('group_id_list', None)
    if group_id_list:
      return group_id_list
