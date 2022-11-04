from setuptools import setup

setup(
  name='nuheat',
  packages=['nuheat'],
  version='1.0.0',
  description='A Python library that allows control of connected NuHeat Signature radiant floor thermostats.',
  author='Derek Brooks',
  author_email='derek@broox.com',
  url='https://github.com/broox/python-nuheat',
  download_url='https://github.com/broox/python-nuheat/archive/1.0.0.tar.gz',
  license='MIT',
  keywords=['nuheat', 'thermostat', 'home automation', 'python'],
  classifiers=[
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3.7',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'Topic :: Home Automation',
  ],
  install_requires=[
    'requests==2.28.1',
  ],
  extras_require={
    'dev': [
      'coveralls==3.3.1',
      'coverage==6.5.0',
      'mock==4.0.3',
      'nose==1.3.7',
      'responses==0.22.0',
    ]
  },
  python_requires=">=3.7",
)
