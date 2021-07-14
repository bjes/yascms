from pyramid.config import Configurator

from .security import SecurityPolicy


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_session_redis')
        config.include('pyramid_jinja2')
        config.add_jinja2_extension('jinja2.ext.loopcontrols')
        config.include('pyramid_tm')
        config.include('pyramid_mailer')
        config.include('pyramid_retry')
        config.include('pyramid_sqlalchemy')

        config.set_default_csrf_options(require_csrf=True)

        config.set_security_policy(SecurityPolicy())

        config.include('.routes')
        config.scan('.views')
        config.scan('.subscribers')
    return config.make_wsgi_app()
