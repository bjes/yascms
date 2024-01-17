from pyramid import testing

from pyramid.authorization import Everyone

from yascms.security import SecurityPolicy


def test_security_policy_identity_should_return_identity():
    request = testing.DummyRequest()

    policy = SecurityPolicy()
    assert policy.identity(request) is None

    user_id = 1234
    policy.remember(request, user_id)
    request.session['user_id'] = user_id
    assert policy.identity(request) == user_id


def test_security_policy_authenticated_userid_should_return_identity():
    request = testing.DummyRequest()

    policy = SecurityPolicy()
    assert policy.authenticated_userid(request) is None

    user_id = 5678
    policy.remember(request, user_id)
    request.session['user_id'] = user_id
    assert policy.authenticated_userid(request) == user_id


def test_effective_principals_should_return_corresponded_group_list():
    request = testing.DummyRequest()

    group_id_list = set([1, 2, 3])
    request.session['group_id_list'] = group_id_list
    policy = SecurityPolicy()

    assert policy.effective_principals(request) == [Everyone] + list(group_id_list)
