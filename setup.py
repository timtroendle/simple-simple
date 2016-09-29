#!/usr/bin/env python3

from setuptools import setup, find_packages

exec(open('simplesimple/__init__.py').read())

setup(
    name='simplesimple',
    version=__version__,
    description='A simple Building Energy Model.',
    maintainer='Tim Tröndle',
    maintainer_email='tt397@cam.ac.uk',
    url='https://www.github.com/timtroendle/simple-simple',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering'
    ]
)
