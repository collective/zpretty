from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name="zpretty",
    version="3.0.0",
    description="An opinionated HTML/XML soup formatter",
    keywords=["Formatter", "HTML", "Prettifier", "Pretty print", "TAL", "XML", "ZPT"],
    long_description="\n".join((read("README.md"), read("HISTORY.md"))),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
    author="Alessandro Pisa",
    author_email="alessandro.pisa@gmail.com",
    url="https://github.com/collective/zpretty",
    license="BSD",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=["setuptools", "beautifulsoup4", "lxml"],
    extras_require={
        "test": ["pre-commit", "pytest-cov", "pytest"],
        "development": ["zest.releaser", "check-manifest", "pyroma"],
    },
    test_suite="zpretty.tests",
    entry_points={"console_scripts": ["zpretty=zpretty.cli:run"]},
    include_package_data=True,
    zip_safe=False,
)
