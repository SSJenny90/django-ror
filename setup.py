#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="django-ror",
    version="0.1.0",
    description="",
    author="Sam Jennings",
    author_email="samuel.scott.jennings@gmail.com",
    url="https://github.com/SSJenny90/django-ror",
    packages=[
        "ror",
    ],
    include_package_data=True,
    install_requires=[
        "django-organizations",
    ],
    license="MIT",
    zip_safe=False,
    keywords="django,organization,geoluminate,research,scientific",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django :: 3.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
