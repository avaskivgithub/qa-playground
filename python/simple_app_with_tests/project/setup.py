
from setuptools import setup
import sys

eggs_list = ['flask==1.1.2',
            'requests==2.21.0',
            'beautifulsoup4==4.9.1',
            'selenium==4.0.0a6.post2',
            'nose==1.3.7',
            'gevent==20.6.2',
            'PyGnuplot']
if sys.version_info < (3,0):
      eggs_list = ['flask',
            'requests',
            'beautifulsoup4',
            'selenium',
            'nose',
            'gevent',
            'PyGnuplot',
            'pysqlite']

setup(name='test-playground',
      version='0.3',
      description='Test playground',
      author='Andriana Vaskiv',
      author_email='andriana.vaskiv@gmail.com',
      install_requires=eggs_list)


# EOF

