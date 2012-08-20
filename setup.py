#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '0.1.2'

setup(
    name='twitterspawn',
    version=version,
    description='Scalable, concurrent requests to the Twitter REST API, that respect Twitter\'s rate limits, using gevent and requests.',
    long_description=open('README.md').read(),
    author='Steve Winton',
    author_email='stevewinton@gmail.com',
    url='https://github.com/swinton/twitterspawn',
    packages=find_packages(),
    install_requires=['gevent==0.13.7', 'greenlet==0.4.0', 'requests-oauth==0.4.1', 'requests==0.13.7'],
    license='BSD',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
    keywords=['requests', 'python-requests', 'gevent', 'twitterspawn'],
    zip_safe=False,
)