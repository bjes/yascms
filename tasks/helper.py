import os

from invoke.exceptions import ParseError


def find_ini_file():
    if os.path.exists('production.ini'):
        return 'production.ini'
    elif os.path.exists('development.ini'):
        return 'development.ini'
    else:
        raise ParseError('--ini-file should be valid file path')
