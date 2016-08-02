#!/usr/bin/env python

from setuptools import setup, find_packages
import sys

py_version = sys.version_info[:2]
print(py_version)
print(find_packages())
if py_version < (3, 3):
    install_requires = ["redis"]

    packages = find_packages(exclude=(
        "websocket_redis.api.async",
        "websocket_redis.server",
    ))
else:
    install_requires = [
        "websockets",
        "aioredis",
        "redis"
    ]
    packages = find_packages()

print(find_packages())
setup(
    name="websocket_redis",
    version="0.0.1",
    description='Communicate with client through '
    'websocket and redis as messaging broker',
    long_description='''
''',
    keywords='python websocket API redis asyncio',
    author='Mohamed abdeljelil',
    author_email="abdeljelil.mohamed@gmail.com",
    url='https://github.com/Abdeljelil/websocket_redis',
    download_url="https://github.com/Abdeljelil/websocket_redis.git",
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.5',
    ],
    packages=packages,
    include_package_data=True,
    extras_require={
    },
    license='BSD',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
        ],
    },
)
