#!/usr/bin/env python3

import setuptools

install_requires = []
with open("requirements.txt", "r", encoding="UTF-8") as f_stream:
    for pack in f_stream:
        install_requires.append(pack)


# setuptools.setup(
#     name="pyggester",
#     version="1.0.0",
#     packages=setuptools.find_packages(),
#     install_requires=install_requires,
#     entry_points={
#         "console_scripts": [
#             "pyggest=pyggester.main:main",
#         ],
#     },
#     include_package_data=True,
# )


setuptools.setup(
    name="pyggester",
    version="1.0.0",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "pyggest=pyggester.main:main",
        ],
    },
    package_data={"pyggester": ["data/*", "data/help_files/*"]},
)
