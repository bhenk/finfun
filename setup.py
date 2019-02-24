from setuptools import setup
import fintec.version as version

setup(
    name='fintec',
    version=version.__version__,
    packages=['fintec'],
    url='https://github.com/bhenk/fintec',
    license='Apache License Version 2.0',
    author='hvdb',
    author_email='',
    description='A collection of utilities to do financial calculations',
    install_requires=['pandas', 'numpy', 'Jinja2', 'requests']
)