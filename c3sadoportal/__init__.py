from pyramid.config import Configurator

from .security.request import RequestWithUserAttribute
from .security import (
    Root,
    groupfinder
)
from pyramid_beaker import session_factory_from_settings
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from trytond.transaction import Transaction
from trytond.pool import Pool

from trytond.config import config
config.update_etc('/ado/etc/trytond.conf')


def get_tryton_pool(request):
    Transaction().start('c3s', 0)
    pool = Pool()

    def _cleanup(request):
        Transaction().stop()
    request.add_finished_callback(_cleanup)
    return pool


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    session_factory = session_factory_from_settings(settings)

    authn_policy = AuthTktAuthenticationPolicy(
        's0secret!!',
        callback=groupfinder,)
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy,
                          session_factory=session_factory,
                          root_factory=Root)
    # using a custom request with user information
    config.set_request_factory(RequestWithUserAttribute)

    # tryton
    Pool.start()
    Pool('c3s').init()
    config.set_request_property(get_tryton_pool, 'tryton_pool', reify=True)

    config.include('cornice')
    config.include('pyramid_chameleon')
    config.include('pyramid_mailer')
    config.add_static_view('static', 'static', cache_max_age=3600)
    # subscriber
    config.add_subscriber(
        'c3sadoportal.subscribers.add_base_bootstrap_template',
        'pyramid.events.BeforeRender')
    config.add_subscriber('c3sadoportal.subscribers.add_locale_to_cookie',
                          'pyramid.events.NewRequest')
    # routes
    config.add_route('login', '/')
    config.add_route('logged_in', '/logged_in')
    config.add_route('logout', '/logout')
    config.add_route('register', '/register')
    config.scan()
    return config.make_wsgi_app()
