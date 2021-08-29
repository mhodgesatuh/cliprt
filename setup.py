#!/usr/bin/env python
"""Setup script for packaging cliprt.

To build a package for distribution:
    python setup.py sdist
and upload it to the PyPI with:
    python setup.py upload

Install a link for development work:
    pip install -e .

The manifest.in file is used for data files.

https://github.com/mhodgesatuh/cliprty
"""
from setuptools import setup, find_packages

setup(name='cliprt',
    version='0.2.0',
    description='Client Information Reporting',
    url='http://github.com/mhodgesatuh/cliprt',
    author='Michael Hodves',
    author_email='mhodges2@gmail.com',
    license='Apache License, Version 2.0',
    packages=find_packages(),
    install_requires=['openpyxl'],
    python_requires=">=3.6, ",
)