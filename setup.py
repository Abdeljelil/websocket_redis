#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="ws_redis",
    version="0.0.1",
    description='',
    long_description='''
''',
    keywords='python websocket API redis asyncio',
    author='Mohamed abdeljelil',
    url='',
    license='',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(),
    include_package_data=True,

    use_2to3=True,
    extras_require={
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
