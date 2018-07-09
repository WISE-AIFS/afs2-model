#!/usr/bin/env python
# encoding: utf-8

import os
import subprocess
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements
from setuptools import setup, find_packages

setup_requirements_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements_setup.txt')
setup_requires = parse_requirements(setup_requirements_path, session='hack')
setup_requires = [str(ir.req) for ir in setup_requires]

tests_requirements_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements_test.txt')
tests_require = parse_requirements(tests_requirements_path, session='hack')
tests_require = [str(ir.req) for ir in tests_require]

requirements_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')
install_requires = parse_requirements(requirements_path, session='hack')
install_requires = [str(ir.req) for ir in install_requires]

version_tag = subprocess.check_output(["git", "describe"]).strip().decode()

setup(
    name='afs',
    version=version_tag,
    description='For AFS developer to develop analytics',
    long_description=open('ReadMe.md').read(),
    author='benchuang',
    author_email='benchuang@iii.org.tw',
    url='https://github.com/benchuang11046/afs',
    license='MIT',
    install_requires=install_requires,
    # packages=['afs'],
    packages=find_packages(exclude=["tests", "test_reports", "prometheus-data", "build"]),
    setup_requires=setup_requires,
    tests_require=tests_require,
    test_suite='nose.collector',
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'iii_afs = afs.__main__:main'
        ]
    },
)
