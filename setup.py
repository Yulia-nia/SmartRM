from os.path import join, dirname
from setuptools import setup, find_packages


setup(
    name='smartRM',
    version='1.0.0',
    author='Yulia Netetskaya',
    author_email='netetskayayulia@gmail.com',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README')).read()
)
