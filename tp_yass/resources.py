import logging

from pyramid.authorization import (Allow,
                                   Everyone,
                                   ALL_PERMISSIONS)

from tp_yass.dal import DAL
from tp_yass.enum import GroupType


logger = logging.getLogger(__name__)


class ACL:
    pass


def admin_factory(request):
    """管理者權限全開"""
    acl = ACL()
    if 'is_admin' in request.session and request.session['is_admin']:
        acl.__acl__ = [(Allow, Everyone, ALL_PERMISSIONS)]
    else:
        acl.__acl__ = []
    return acl


def auth_user_factory(request):
    """只要有登入，不管是一般帳號還是管理者帳號，都會存在 groups 這個 session，直接給過"""
    acl = ACL()
    if 'groups' in request.session:
        logger.debug('比對群組權限接受，權限為已有帳號的身份')
        acl.__acl__ = [(Allow, Everyone, ALL_PERMISSIONS)]
    else:
        acl.__acl__ = []
    return acl


def page_edit_factory(request):
    """單一頁面所屬的群組（們）才有後台編輯的權限"""
    acl = ACL()
    page_id = int(request.matchdict['page_id'])
    logger.debug('page_id 為 %s', page_id)
    page = DAL.get_page(page_id)
    if page:
        # 若為管理者，權限全開
        if request.session.get('is_admin'):
            logger.debug('比對群組權限接受，權限為管理者')
            page.__acl__ = [(Allow, Everyone, ALL_PERMISSIONS)]
        # 否則只有 page 的群組有 edit 權限
        else:
            logger.debug('比對群組權限接受，權限為對應單一頁面的群組')
            page.__acl__ = []
            for each_group in page.groups:
                logger.debug('群組 %s 可編輯此單一頁面', each_group.name)
                page.__acl__.append((Allow, each_group.id, 'edit'))
    else:
        logger.error('找不到 page id 為 %s 的單一頁面，群組權限比對異常', page_id)
        acl.__acl__ = []
    return page or acl


def staff_group_factory(request):
    """只有管理者或使用者擁有行政群組才有權限"""
    acl = ACL()
    acl.__acl__ = []
    if 'groups' in request.session:
        for each_sub_group in request.session['groups']:
            for each_group in each_sub_group:
                if each_group['type'] in (GroupType.ADMIN, GroupType.STAFF):
                    acl.__acl__ = [(Allow, Everyone, ALL_PERMISSIONS)]
                    return acl
    return acl


def news_edit_factory(request):
    """最新消息只有建立的群組與管理者可以刪除或修改"""
    acl = ACL()
    news_id = int(request.matchdict['news_id'])
    logger.debug('news_id 為 %s', news_id)
    news = DAL.get_news(news_id)
    if news:
        # 若為管理者，權限全開
        if 'is_admin' in request.session and request.session['is_admin']:
            logger.debug('比對群組權限接受，權限為管理者')
            news.__acl__ = [(Allow, Everyone, ALL_PERMISSIONS)]
        # 否則只有 news 的群組有 edit 權限
        else:
            logger.debug('比對群組權限接受，權限為對應最新消息的群組')
            logger.debug('群組 %s 可編輯最新消息', news.group.name)
            news.__acl__ = [(Allow, news.group.id, 'edit')]
    else:
        logger.error('找不到 news id 為 %s 的最新消息，群組權限比對異常', news_id)
        acl.__acl__ = []
    return news or acl


def link_edit_factory(request):
    """好站連結只有建立的群組與管理者可以刪除或修改"""
    acl = ACL()
    link_id = int(request.matchdict['link_id'])
    logger.debug('link_id 為 %s', link_id)
    link = DAL.get_link(link_id)
    if link:
        # 若為管理者，權限全開
        if 'is_admin' in request.session and request.session['is_admin']:
            logger.debug('比對群組權限接受，權限為管理者')
            link.__acl__ = [(Allow, Everyone, ALL_PERMISSIONS)]
        # 否則只有 link 的群組有 edit 權限
        else:
            logger.debug('比對群組權限接受，權限為對應最新消息的群組')
            logger.debug('群組 %s 可編輯最新消息', link.group.name)
            link.__acl__ = [(Allow, link.group.id, 'edit')]
    else:
        logger.error('找不到 link id 為 %s 的最新消息，群組權限比對異常', link_id)
        acl.__acl__ = []
    return link or acl
