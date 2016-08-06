#!/usr/bin/env python
import os
import sys

from setuptools import find_packages, setup

version = ("0", "0", "8")


root = os.path.dirname(__file__)
readme_file = os.path.join(root, 'README.md')

if os.path.isfile(readme_file):
    with open(readme_file) as f:
        long_description = '\n\n'.join(f.read().split('\n\n')[1:])
else:
    long_description = ""

py_version = sys.version_info[:2]

if py_version < (3, 3):

    install_requires = ["redis"]

    packages = find_packages(exclude=(
        "websocket_redis.common.aioredis",
        "websocket_redis.api.async",
        "websocket_redis.server",
        "tests"
    ))
else:

    install_requires = [
        "websockets",
        "aioredis",
        "redis"
    ]

    packages = find_packages(exclude=("tests"))

setup(
    name="websocket_redis",
    version=".".join(version),
    description='Communicate with websocket through redis as messaging broker',
    long_description=long_description,
    keywords='python websocket redis asyncio',
    author='Mohamed abdeljelil',
    author_email="abdeljelil.mohamed@gmail.com",
    url='https://github.com/Abdeljelil/websocket_redis',
    download_url="https://github.com/Abdeljelil/websocket_redis.git",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=packages,
    include_package_data=True,
    extras_require={
        ':python_version=="3.3"': ['asyncio'],
    },
    license='BSD',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
        ],
    },
)

print(py_version)
print(packages)
print(install_requires)
print(version)
