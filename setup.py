#!/usr/bin/env python
from setuptools import setup, find_packages
from codecs import open
from os import path

directory = path.abspath(path.dirname(__file__))

from pyMAPPINGS.version import __version__
with open(path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='pyMAPPINGS',
      version=__version__,
      description='Python library to run and analyze MAPPINGS photoionization models.',
      long_description=long_description,
      author='Teja Teppala',
      author_email='teja.teppala@gmail.com',
      maintainer='Teja Teppala',
      maintainer_email='teja.teppala@gmail.com', 
      license='GPL',
      keywords="astronomy photoionization mappings"
     )
