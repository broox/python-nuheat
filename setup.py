from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
  name='nuheat',
  packages=['nuheat'],
  version='1.1.0',
  description='A Python library that allows control of connected NuHeat Signature and Mapei Mapeheat radiant floor thermostats.',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author='Derek Brooks',
  author_email='derek@broox.com',
  url='https://github.com/broox/python-nuheat',
  download_url='https://github.com/broox/python-nuheat/archive/1.1.0.tar.gz',
  license='MIT',
  keywords=['nuheat', 'thermostat', 'home automation', 'python'],
  classifiers=[
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3.9',
      'Programming Language :: Python :: 3.10',
      'Programming Language :: Python :: 3.11',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'Topic :: Home Automation',
  ],
  install_requires=[
    'requests>=2.28.1',
  ],
  extras_require={
    'dev': [
      'coveralls==3.3.1',
      'coverage==6.5.0',
      'parameterized==0.8.1',
      'pytest==7.2.0',
      'pytest-cov==4.0.0',
      'responses==0.22.0',
    ]
  },
  python_requires=">=3.7",
)
