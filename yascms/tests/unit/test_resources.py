from pyramid import testing
from pyramid.authorization import (Allow,
                                   Everyone,
                                   ALL_PERMISSIONS)

from yascms import resources
from yascms.enum import GroupType


def test_admin_factory_with_request_should_return_acl():
    request = testing.DummyRequest()

    # anonymous and normal user
    acl = resources.admin_factory(request)
    assert acl.__acl__ == []

    # admin
    request.session['is_admin'] = True
    acl = resources.admin_factory(request)
    assert acl.__acl__ == [(Allow, Everyone, ALL_PERMISSIONS)]


def test_auth_user_factory_with_request_should_return_acl():
    request = testing.DummyRequest()

    # anonymous
    acl = resources.admin_factory(request)
    assert acl.__acl__ == []

    # normal user and admin
    request.session['groups'] = 999
    acl = resources.auth_user_factory(request)
    assert acl.__acl__ == [(Allow, Everyone, ALL_PERMISSIONS)]


def test_staff_group_factory_with_request_should_return_acl():
    request = testing.DummyRequest()

    # anonymous
    acl = resources.staff_factory(request)
    assert acl.__acl__ == []

    # non staff groups
    request.session['groups'] = [[{'type': GroupType.NORMAL}]]
    acl = resources.staff_factory(request)
    assert acl.__acl__ == []

    # staff groups
    request.session['groups'] = [[{'type': GroupType.STAFF}]]
    acl = resources.staff_factory(request)
    assert acl.__acl__ == [(Allow, Everyone, ALL_PERMISSIONS)]

    # admin groups
    request.session['groups'] = [[{'type': GroupType.ADMIN}]]
    acl = resources.staff_factory(request)
    assert acl.__acl__ == [(Allow, Everyone, ALL_PERMISSIONS)]


def test_page_edit_factory_with_request_should_return_acl(mocker):
    request = testing.DummyRequest()
    request.matchdict['page_id'] = 999

    # page not found
    mocker.patch.object(resources.DAL, "get_page", return_value=None)
    acl = resources.page_edit_factory(request)
    assert acl.__acl__ == []

    # fake page
    page = mocker.MagicMock()
    page_group = mocker.MagicMock()
    page_group.name = 'foo'
    page_group.id = 123
    page.groups = [page_group]

    mocker.patch.object(resources.DAL, "get_page", return_value=page)

    # fake page with anonymous or normal user
    acl = resources.page_edit_factory(request)
    assert acl.__acl__ == [(Allow, page_group.id, 'edit')]

    # fake page with admin
    request.session['is_admin'] = True
    acl = resources.page_edit_factory(request)
    assert acl.__acl__ == [(Allow, Everyone, ALL_PERMISSIONS)]


def test_news_edit_factory_with_request_should_return_acl(mocker):
    request = testing.DummyRequest()
    request.matchdict['news_id'] = 999

    # news not found
    mocker.patch.object(resources.DAL, "get_news", return_value=None)
    acl = resources.news_edit_factory(request)
    assert acl.__acl__ == []

    # fake news
    news = mocker.MagicMock()
    news.group.name = 'foo'
    news.group.id = 123

    mocker.patch.object(resources.DAL, "get_news", return_value=news)

    # fake news with anonymous or normal user
    acl = resources.news_edit_factory(request)
    assert acl.__acl__ == [(Allow, news.group.id, 'edit')]

    # fake news with admin
    request.session['is_admin'] = True
    acl = resources.news_edit_factory(request)
    assert acl.__acl__ == [(Allow, Everyone, ALL_PERMISSIONS)]


def test_link_edit_factory_with_request_should_return_acl(mocker):
    request = testing.DummyRequest()
    request.matchdict['link_id'] = 999

    # link not found
    mocker.patch.object(resources.DAL, "get_link", return_value=None)
    acl = resources.link_edit_factory(request)
    assert acl.__acl__ == []

    # fake link
    link = mocker.MagicMock()
    link.group.name = 'foo'
    link.group.id = 123

    mocker.patch.object(resources.DAL, "get_link", return_value=link)

    # fake link with anonymous or normal user
    acl = resources.link_edit_factory(request)
    assert acl.__acl__ == [(Allow, link.group.id, 'edit')]

    # fake link with admin
    request.session['is_admin'] = True
    acl = resources.link_edit_factory(request)
    assert acl.__acl__ == [(Allow, Everyone, ALL_PERMISSIONS)]


def test_api_token_factory_should_return_proper_acl(mocker):
    request = testing.DummyRequest()
    # 測試沒有 Authorization header
    assert resources.api_token_factory(request).__acl__ == []

    # 測試有 Authorization header 但驗證沒過
    request.headers['Authorization'] = 'foo'
    mocker.patch.object(resources.DAL, 'get_api_token', return_value=False)
    assert resources.api_token_factory(request).__acl__ == []

    # 測試有正常的 Authorization header 且驗證通過
    mocker.patch.object(resources.DAL, 'get_api_token', return_value=True)
    assert resources.api_token_factory(request).__acl__ == [(Allow, Everyone, ALL_PERMISSIONS)]
