#! /usr/bin/env python

from setuptools import setup

setup(
    name='convertbleswitch',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author='Liran Piade',
    author_email='liranpiade@gmail.com',
    python_requires='>=3.8',
    packages=['convertbleswitch'],
    entry_points={
        'console_scripts': [
            'setsysmode = convertbleswitch.cli:main'
        ],
    },
    url='https://github.com/conqp/tablet-mode',
    license='GPLv3',
    description='Tablet mode switch for libinput.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords='tablet mode tent convertible switch'
)
