#! /usr/bin/env python

from setuptools import setup

setup(
    name='convertibleswitch',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author='Liran Piade',
    author_email='liranpiade@gmail.com',
    python_requires='>=3.8',
    packages=['convertbleswitch'],
    entry_points={
        'console_scripts': [
            'setsysmode = convertibleswitch.cli:main'
        ],
    },
    url='https://github.com/lirannl/convertible-switch',
    license='GPLv3',
    description='Tablet mode switch for libinput. Devices are controlled at a kernel level, so that the DE can properly detect tablet mode usage',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords='tablet mode tent convertible switch'
)
