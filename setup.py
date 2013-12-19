# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Setup script for installing nice_hotqueue.
"""

import os
import sys

from setuptools import setup, find_packages


try:
    SETUP_DIRNAME = os.path.dirname(__file__)
except NameError:
    SETUP_DIRNAME = os.path.dirname(sys.argv[0])

if SETUP_DIRNAME != '':
    os.chdir(SETUP_DIRNAME)

SETUP_DIR = os.path.abspath(SETUP_DIRNAME)
REQUIREMENTS_DIR = os.path.join('requirements')
INSTALL_REQS = os.path.join(REQUIREMENTS_DIR, 'install.txt')
TEST_REQS = os.path.join(REQUIREMENTS_DIR, 'test.txt')
DEVELOPMENT_REQS = os.path.join(REQUIREMENTS_DIR, 'development.txt')


def read(fname):
    return open(fname).read()


def get_reqs(filename):
    reqs = []
    with open(filename) as handle:
        for line in handle.readlines():
            if not line or line.startswith('#'):
                continue
            reqs.append(line.strip())
    return reqs

install_requires = get_reqs(INSTALL_REQS)
test_requires = install_requires + get_reqs(TEST_REQS)
dev_requires = test_requires + get_reqs(DEVELOPMENT_REQS)

setup(
    name='nice_hotqueue',
    version='0.1.0',
    author='Ben Jackson',
    author_email='ben@adaptivelab.co.uk',
    url='https://github.com/adaptivelab/nice_hotqueue',
    license='LICENSE.txt',
    description='HotQueue Wrapper that sleeps if the queue is too full.',
    long_description=read('README.txt'),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    # Module Dependencies
    install_requires=install_requires,
    extras_require={
        'test': test_requires,
        'dev': dev_requires},
    dependency_links=[
        'http://pypi.adaptivelab.co.uk/simple'],
    # Classifiers for Package Indexing
    classifiers=[
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules'])
