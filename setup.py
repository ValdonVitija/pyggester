#!/usr/bin/env python3

import setuptools

install_requires = []

setuptools.setup(
    name="pyggester",
    version="1.0.0",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'pyggest=pyggester.main:main',
        ],
    },
    include_package_data=True,
    )

