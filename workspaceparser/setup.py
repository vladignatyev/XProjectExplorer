# coding: utf-8
__author__ = 'ya.na.pochte@gmail.com'

from distutils.core import setup
from distutils.command.install import install
from setuptools import find_packages
import os.path

with open('requirements.pip') as f:
    required = f.read().splitlines()

setup(name="workspaceparser",
      author="Vladimir Ignatev",
      author_email="ya.na.pochte@gmail.com",
      url="http://macbuildserver.com",
      version="0.1",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=required
)
