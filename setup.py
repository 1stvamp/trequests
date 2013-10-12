"""Installer for trequests
"""

from os import path
try:
        from setuptools import setup, find_packages
except ImportError:
        from ez_setup import use_setuptools
        use_setuptools()
        from setuptools import setup, find_packages


cwd = path.dirname(__file__)
__version__ = open(path.join(cwd, 'trequests_version.txt'),
                   'r').read().strip()

setup(
    name='trequests',
    description='A Tornado async HTTP/HTTPS client '
                'adaptor for python-requests',
    long_description=open('README.rst').read(),
    version=__version__,
    author='Wes Mason',
    author_email='wes@1stvamp.org',
    url='https://github.com/1stvamp/trequests',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=open('requirements.txt').readlines(),
    package_data={'': ['trequests_version.txt']},
    include_package_data=True,
    license='BSD'
)
