from distutils.core import setup

setup(
    name='nice_hotqueue',
    version='0.0.1',
    author='Ben Jackson',
    author_email='ben@adaptivelab.co.uk',
    packages=['nice_hotqueue', 'nice_hotqueue.test'],
    scripts=[],
    url='https://github.com/adaptivelab/nice_hotqueue',
    license='LICENSE.txt',
    description='Wrapper around HotQueue that sleeps if the queue is too full.',
    long_description=open('README.txt').read(),
    install_requires=[],
)
