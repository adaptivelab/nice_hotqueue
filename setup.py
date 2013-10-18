import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='nice_hotqueue',
    version='0.1.0',
    author='Ben Jackson',
    author_email='ben@adaptivelab.co.uk',
    packages=['nice_hotqueue', 'nice_hotqueue.test'],
    scripts=[],
    url='https://github.com/adaptivelab/nice_hotqueue',
    license='LICENSE.txt',
    description='Wrapper around HotQueue that sleeps if the queue is too full.',
    long_description=read('README.txt'),
    install_requires=[
        'hotqueue==0.2.7'
    ],
)
