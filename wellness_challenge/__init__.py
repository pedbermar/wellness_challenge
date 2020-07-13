from pyramid.config import Configurator
from pymongo import MongoClient
from urllib.parse import urlparse
from pyramid.authorization import ACLAuthorizationPolicy


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    
    # Pyramid requires an authorization policy to be active.
    config.set_authorization_policy(ACLAuthorizationPolicy())
    # Enable JWT authentication.
    config.include('pyramid_jwt')
    config.set_jwt_authentication_policy('secret')
    
    db_url = urlparse(settings['mongo_uri'])
    config.registry.db = MongoClient(
        host=db_url.hostname,
        port=db_url.port,
    )

    def add_db(request):
        db = config.registry.db[db_url.path[1:]]
        if db_url.username and db_url.password:
           db.authenticate(db_url.username, db_url.password)
        return db

    config.include('pyramid_beaker')
    
    config.add_request_method(add_db, 'db', reify=True)

    config.add_route('index', '/')
    config.add_route('load_csv', '/load_csv')
    config.add_route('metrics', '/metrics/{type}/{startDate}/{endDate}')
    config.add_route('current_month', '/current_month')
    config.add_route('daily', '/daily/{type}')
    config.add_route('login', '/login')
    config.scan()
    return config.make_wsgi_app()
