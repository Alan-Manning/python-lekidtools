========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |github-actions| |codecov|
    * - package
      - |version| |wheel| |supported-versions| |supported-implementations| |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-lekidtools/badge/?style=flat
    :target: https://readthedocs.org/projects/python-lekidtools/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/Alan-Manning/python-lekidtools/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/Alan-Manning/python-lekidtools/actions

.. |codecov| image:: https://codecov.io/gh/Alan-Manning/python-lekidtools/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://app.codecov.io/github/Alan-Manning/python-lekidtools

.. |version| image:: https://img.shields.io/pypi/v/lekidtools.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/lekidtools

.. |wheel| image:: https://img.shields.io/pypi/wheel/lekidtools.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/lekidtools

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/lekidtools.svg
    :alt: Supported versions
    :target: https://pypi.org/project/lekidtools

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/lekidtools.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/lekidtools

.. |commits-since| image:: https://img.shields.io/github/commits-since/Alan-Manning/python-lekidtools/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/Alan-Manning/python-lekidtools/compare/v0.0.0...main



.. end-badges

simple tools for python work with LEKIDs

* Free software: GNU Lesser General Public License v3 or later (LGPLv3+)

Installation
============

::

    pip install lekidtools

You can also install the in-development version with::

    pip install https://github.com/Alan-Manning/python-lekidtools/archive/main.zip


Documentation
=============


https://python-lekidtools.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
