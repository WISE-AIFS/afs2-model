#!/usr/bin/env python
# encoding: utf-8

import os

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements
from setuptools import setup, find_packages

dev_requirements_path = os.path.join(os.path.dirname(__file__), 'requirements_dev.txt')
dev_requires = parse_requirements(dev_requirements_path, session='hack')
dev_requires = [str(ir.req) for ir in dev_requires]

requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
install_requires = parse_requirements(requirements_path, session='hack')
install_requires = [str(ir.req) for ir in install_requires]

with open(os.path.join(os.path.dirname(__file__), 'VERSION'), 'r') as f:
    version = f.read()

with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
    long_description = f.read()


setup(
    name='afs2-model',
    version=version,
    description='For AFS developer to develop',
    long_description=long_description,
    author='benchuang, chenjr',
    author_email='ben2019.chuang.advantech.com.tw, chenjr0719@gmail.com',
    url='https://github.com/benchuang11046/afs2-model',
    license='MIT',
    install_requires=install_requires,
    packages=find_packages(exclude=["tests", "test_reports"]),
    zip_safe=False,
    keywords=['afs2', 'WISE-PaaS', 'EI-PaaS'],
    entry_points='''
        [console_scripts]
        eipaas-afs=afs2_model.cli:cli
    ''',
    extras_require={
        'dev': dev_requires,
        'cli': [
            'click'
        ]
    },
    include_package_data = True,
)

# build wheel pacakge
# command: python setup.py bdist_wheel

# build tgz
# command: python setup.py sdist

# clone afs-docs
# git clone --recursive  https://github.com/chenjr0719/AFS-docs.git

# pull docs from afs-sdk
# git submodule foreach git pull origin master

# upload to pypyi
# twine upload --repository-url [url] [.whl]
