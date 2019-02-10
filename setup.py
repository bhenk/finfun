from setuptools import setup
import finfun.version as version

setup(
    name='finfun',
    version=version.__version__,
    packages=['finfun'],
    url='https://github.com/bhenk/finfun',
    license='Apache License Version 2.0',
    author='hvdb',
    author_email='',
    description='A collection of utilities to do financial calculations',
    install_requires=['pandas', 'numpy']
)