from setuptools import setup

setup(
    name='finfun',
    version='0.0.1',
    packages=['finfun', 'finfun.finfun'],
    url='https://github.com/bhenk/finfun',
    license='Apache License Version 2.0',
    author='hvdb',
    author_email='',
    description='A collection of utilities to do financial calculations',
    install_requires=['pandas', 'numpy']
)