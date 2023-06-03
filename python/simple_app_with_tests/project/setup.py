
from setuptools import setup
import sys

eggs_list = ['flask>=2.2.2',
            'requests==2.21.0',
            'beautifulsoup4==4.9.1',
            'selenium',
            'gevent',
            'pytest',
            'zipp',
            'typing-extensions',
            'urllib3==1.26.6',
            'chardet',
            'idna',
            'paramiko',
            'cryptography>=3.3']
if sys.version_info < (3,0):
      eggs_list = ['flask',
            'requests',
            'beautifulsoup4',
            'selenium',
            'gevent',
            'pysqlite',
            'pytest',
            'zipp']

setup(name='test-playground',
      version='0.4',
      description='Test playground',
      author='Andriana Vaskiv',
      author_email='andriana.vaskiv@gmail.com',
      install_requires=eggs_list)


# EOF

