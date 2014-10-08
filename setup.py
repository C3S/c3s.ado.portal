import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'colander',
    'cornice',
    'coverage',
    'cryptacular',
    'deform==2.0a2',
    'nose',
    'pyramid',
    'pyramid_beaker',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_mailer',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'webtest',
]

setup(name='c3s.ado.portal',
      version='0.0',
      description='c3s.ado.portal',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='c3sadoportal',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = c3sadoportal:main
      [console_scripts]
      initialize_c3s.ado.portal_db = c3sadoportal.scripts.initializedb:main
      """,
      )
