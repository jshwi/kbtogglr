kbtogglr
========
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License
.. image:: https://img.shields.io/pypi/v/kbtogglr
    :target: https://pypi.org/project/kbtogglr/
    :alt: PyPI
.. image:: https://github.com/jshwi/kbtogglr/actions/workflows/build.yaml/badge.svg
    :target: https://github.com/jshwi/kbtogglr/actions/workflows/build.yaml
    :alt: Build
.. image:: https://github.com/jshwi/kbtogglr/actions/workflows/codeql-analysis.yml/badge.svg
    :target: https://github.com/jshwi/kbtogglr/actions/workflows/codeql-analysis.yml
    :alt: CodeQL
.. image:: https://results.pre-commit.ci/badge/github/jshwi/kbtogglr/master.svg
   :target: https://results.pre-commit.ci/latest/github/jshwi/kbtogglr/master
   :alt: pre-commit.ci status
.. image:: https://codecov.io/gh/jshwi/kbtogglr/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jshwi/kbtogglr
    :alt: codecov.io
.. image:: https://readthedocs.org/projects/kbtogglr/badge/?version=latest
    :target: https://kbtogglr.readthedocs.io/en/latest/?badge=latest
    :alt: readthedocs.org
.. image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://www.python.org/downloads/release/python-380
    :alt: python3.8
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black
.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/
    :alt: isort
.. image:: https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg
    :target: https://github.com/PyCQA/docformatter
    :alt: docformatter
.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/PyCQA/pylint
    :alt: pylint
.. image:: https://img.shields.io/badge/security-bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status
.. image:: https://snyk.io/test/github/jshwi/kbtogglr/badge.svg
    :target: https://snyk.io/test/github/jshwi/kbtogglr/badge.svg
    :alt: Known Vulnerabilities
.. image:: https://snyk.io/advisor/python/kbtogglr/badge.svg
    :target: https://snyk.io/advisor/python/kbtogglr
    :alt: kbtogglr

Toggle keyboard on and off
--------------------------

Simple app designed to toggle laptop keyboard on and off when using a USB keyboard

Prerequisites
-------------
    | Python3
    | This package has only been tested on Gnome

Dependencies
------------
xinput

    Debian, Ubuntu etc:

    .. code-block:: console

        $ sudo apt install xinput

    RHEL, Fedora etc:

    .. code-block:: console

        $ sudo dnf install xinput

Install
-------
.. code-block:: console

    $ pip install kbtogglr --user

The app should be available in your applications
