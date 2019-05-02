import os

from pyramid.paster import get_app, setup_logging


dir_path = os.path.dirname(__file__)
ini_path = os.path.join(dir_path, 'production.ini')
setup_logging(ini_path)
application = get_app(ini_path, 'main')

