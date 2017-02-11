# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name='zpretty',
    version='0.9.0',
    description='An opinionated HTML/XML soup formatter',
    keywords=[
        'Formatter',
        'HTML',
        'Prettifier',
        'Pretty print',
        'TAL',
        'XML',
        'ZPT',
    ],
    long_description='\n'.join((
        read('README.rst'),
        read('HISTORY.rst'),
    )),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
    ],
    author='Alessandro Pisa',
    author_email='alessandro.pisa@gmail.com',
    url='https://github.com/collective/zpretty',
    license='BSD',
    packages=find_packages(),
    install_requires=[
        'setuptools',
        'beautifulsoup4',
    ],
    extras_require={
        'test': [
            'nose',
            'nose-selecttests',
            'rednose',
            'coverage',
            'unittest2',
            'flake8',
        ],
        'development': [
            'zest.releaser',
            'check-manifest',
            'pyroma',
        ],
    },
    test_suite="zpretty.tests",
    entry_points={
        'console_scripts': [
            'zpretty=zpretty.cli:run',
        ]
    },
    include_package_data=True,
    zip_safe=False,
)
