#!/usr/bin/env python
# encoding: utf-8

import os
import pathlib
from setuptools import setup, find_packages
import pkg_resources

with pathlib.Path('requirements_dev.txt').open() as requirements_txt:
    dev_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]


with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

with open(os.path.join(os.path.dirname(__file__), "VERSION"), "r") as f:
    version = f.read()

with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as f:
    long_description = f.read()

setup(
    name="afs2-model",
    version=version,
    description="For AFS developer to develop analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="WISE-PaaS/AFS",
    author_email="ben2019.chuang@advantech.com.tw",
    url="https://github.com/benchuang11046/afs2-model",
    license="Apache License 2.0",
    install_requires=install_requires,
    packages=find_packages(exclude=["tests", "test_reports"]),
    tests_require=dev_requires,
    zip_safe=False,
    keywords=[
        "AFS",
        "WISE-PaaS",
        "AI framework service",
        "ADVANTECH",
    ],
    entry_points="""
        [console_scripts]
        eipaas-afs=afs.cli:cli
    """,
    include_package_data=True,
)

# build wheel pacakge
# command: python setup.py bdist_wheel

# upload to pypyi
# twine upload --repository-url [url] [.whl]
