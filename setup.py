#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from libcryptomarket import __version__

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pandas>=0.20.0',
    'requests'
]

setup_requirements = [
    'pytest-runner',
    # TODO(gavincyi): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='libcryptomarket',
    version=__version__,
    description="Library for cryptocurrency market information.",
    long_description=readme + '\n\n' + history,
    author="Gavin Chan",
    author_email='gavincyi@gmail.com',
    url='https://github.com/gavincyi/libcryptomarket',
    packages=find_packages(include=['libcryptomarket']),
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='libcryptomarket',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
