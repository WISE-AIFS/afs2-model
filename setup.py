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
    version='1.0.0',
    description='For AFS developer develop analytics',
    long_description=open('README').read(),
    author='Owen Lu, benchuang',
    author_email='benchuang@iii.org.tw',
    url='http://140.92.25.64:8888/estherxchl/afs_project.git',
    license='MIT',
    install_requires=install_requires,
    packages=['afs'],
)