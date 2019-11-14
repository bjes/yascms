import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'invoke',
    'pyramid',
    'pyramid_beaker',
    'pyramid_debugtoolbar',
    'pyramid_ipython',
    'pyramid_mailer',
    'pyramid_jinja2',
    'waitress',
    'PyMySQL',
    'alembic',
    'pyramid_retry',
    'pyramid_sqlalchemy',
    'pyramid_tm',
]

tests_require = [
    'WebTest',
    'mixer',
    'pytest',
    'pytest-cov',
    'pytest-mock',
    'tox',
]

setup(
    name='tp_yass',
    version='0.0',
    description='tp_yass',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Framework :: Pyramid',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = tp_yass:main',
        ],
        'console_scripts': [
            'initialize_tp_yass_db=tp_yass.scripts.initialize_db:main',
        ],
    },
)
