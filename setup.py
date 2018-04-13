#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages
import os
from pip.req import parse_requirements

requirements_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')
install_requires = parse_requirements(requirements_path, session='hack')
install_requires = [str(ir.req) for ir in install_requires]

setup(
    name='afs',
    version='1.1.4',
    description='For AFS developer develop analytics',
    long_description=open('README').read(),
    author='Owen Lu, benchuang',
    author_email='benchuang@iii.org.tw',
    url='https://github.com/benchuang11046/afs',
    license='MIT',
    install_requires=install_requires,
    packages=['afs'],
)