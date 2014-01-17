# -*- coding: utf-8 -*-

# Test by running: pip install -e .[subs]

import sys
from setuptools import setup

major, minor, micro = sys.version_info[:3]

install_requires26 = [
    'flask==0.9.0'
]

subdep26 = [
    'werkzeug==0.7'
]

install_requires27 = [
    'flask==0.10.1'
]

subdep27 = [
    # Flask 0.10.1 requires werkzeug>=0.7 but this succeeds and installs anyway
    'werkzeug==0.6.2'
]


if minor == 7:
    ir = install_requires27
    sr = subdep27
else:
    ir = install_requires26
    sr = subdep26


setup(
    name='test-me',
    version='0.0.1',
    description='Conditional dependencies',
    url='',
    author='Peter M. Elias',
    author_email='petermelias@gmail.com',
    license='MIT',
    install_requires=ir,
    extras_require={
        'subs': sr
    }
)
