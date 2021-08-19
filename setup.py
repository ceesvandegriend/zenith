#!/usr/bin/env python3

"""
Usage: ./setup.py install --user
"""

from setuptools import setup

setup(name='zenith',
      version='0.1',
      description='Project tracking software',
      author='Cees van de Griend',
      author_email='c.vande.griend@gmail.com',
      url='https://github.com/ceesvandegriend/zenith/',
      packages=[
          'zenith',
          'zenith.cli',
          'zenith.command',
          'zenith.factory',
      ],
      install_requires=[
          'SQLAlchemy',
      ],
      )
