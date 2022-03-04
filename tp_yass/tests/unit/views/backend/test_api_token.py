from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPFound

from tp_yass.views.backend import api_token


def test_backend_api_token_list_view_should_return_api_token_list(pyramid_config, mocker):
    mocker.patch.object(api_token.DAL, 'get_api_token_list')
    request = DummyRequest()
    request.effective_theme_name = 'foo'
    assert 'api_token_list' in api_token.APITokenListView(request).get_view()


def test_backend_api_token_create_get_view_should_return_form(pyramid_config):
    request = DummyRequest()
    request.effective_theme_name = 'foo'
    assert 'form' in api_token.APITokenCreateView(request).get_view()


def test_backend_api_token_create_post_view_should_return_form(pyramid_config, mocker):
    request = DummyRequest()
    request.effective_theme_name = 'foo'
    mock_form = mocker.MagicMock()
    mock_form.validate.return_value = True
    mocker.patch.object(api_token, 'APITokenForm', return_value=mock_form)
    mocker.patch.object(api_token, 'DAL', autospec=True)
    response = api_token.APITokenCreateView(request).post_view()
    assert isinstance(response, HTTPFound)
    assert response.status_int == 302
    api_token.DAL.create_api_token.assert_called_once()
    api_token.DAL.save_api_token.assert_called_once()

    mock_form.validate.return_value = False
    mocker.patch.object(api_token, 'APITokenForm', return_value=mock_form)
    response = api_token.APITokenCreateView(request).post_view()
    assert isinstance(response, dict)
    assert 'form' in response
