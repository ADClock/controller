#!/usr/bin/env python

import setuptools
import controller

with open('requirements.txt') as file:
    packages = filter(lambda x: x != "" and x[0] != "#", file.readlines())

with open('README.md') as file:
    description = file.read()

setuptools.setup(
    name='controller',
    version=controller.__version__,
    author='ADClock',
    # author_email='',
    description='Default description for controller.',
    long_description=description,
    long_description_content_type="text/markdown",
    url='https://github.com/ADClock/controller',
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=packages,
    setup_requires=['setuptools']
)
