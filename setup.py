from setuptools import setup

setup(
  name = 'nuheat',
  packages = ['nuheat'],
  version = '0.1.2',
  description = 'A Python library that allows control of connected NuHeat Signature radiant floor thermostats.',
  author = 'Derek Brooks',
  author_email = 'derek@broox.com',
  url = 'https://github.com/broox/python-nuheat',
  download_url = 'https://github.com/broox/python-nuheat/archive/0.1.2.tar.gz',
  license = 'MIT',
  keywords = ['nuheat', 'thermostat', 'home automation', 'python'],
  classifiers = [
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'Topic :: Home Automation'
  ],
)