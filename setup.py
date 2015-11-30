# encoding: utf-8
from setuptools import setup, find_packages
from eureka_client import __version__ as version

setup(
    name='eureka-client',
    version=version,
    description='A python interface for Netflix Eureka',
    author=u'Jorge Dias',
    author_email='jorge@mrdias.com',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=[]),
    install_requires=[
        'dnspython'
    ],
)
