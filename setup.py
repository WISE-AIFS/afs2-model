#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

setup(
    name='afs',
    version='1.0.0',
    description='For AFS developer develop analytics',
    long_description=open('README').read(),
    author='Owen Lu, benchuang',
    author_email='benchuang@iii.org.tw',
    url='http://140.92.25.64:8888/estherxchl/afs_project.git',
    license='MIT',
    install_requires=['setuptools'],
    packages=['afs'],
)