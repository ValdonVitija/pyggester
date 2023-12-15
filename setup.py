#!/usr/bin/env python3

import setuptools

install_requires = []
with open("requirements.txt", "r", encoding="UTF-8") as f_stream:
    for pack in f_stream:
        install_requires.append(pack)


setuptools.setup(
    name="pyggester",
    version=open("VERSION").read().strip(),
    packages=setuptools.find_packages(include=["pyggester", "pyggester.*"]),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Valdon Vitija",
    author_email="valdonvitijaa@gmail.com",
    license="MIT",
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "pyggest=pyggester.main:main",
        ],
    },
    package_data={"pyggester": ["data/*", "data/help_files/*"]},
)
