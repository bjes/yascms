from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .security import group_finder
from .resources import Resource


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_beaker')
        config.include('pyramid_jinja2')
        config.include('pyramid_tm')
        config.include('pyramid_mailer')
        config.include('pyramid_retry')
        config.include('pyramid_sqlalchemy')

        config.set_default_csrf_options(require_csrf=True)

        authn_policy = AuthTktAuthenticationPolicy(settings['auth.secret'],
                                                   callback=group_finder,
                                                   hashalg='sha512')
        authz_policy = ACLAuthorizationPolicy()
        config.set_authentication_policy(authn_policy)
        config.set_authorization_policy(authz_policy)

        config.include('.routes')
        config.scan('.views')
    return config.make_wsgi_app()
