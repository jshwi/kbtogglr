kbtogglr
========
.. image:: https://github.com/jshwi/kbtogglr/workflows/ci/badge.svg
    :target: https://github.com/jshwi/kbtogglr/workflows/ci/badge.svg
    :alt: audit
.. image:: https://github.com/jshwi/kbtogglr/actions/workflows/codeql-analysis.yml/badge.svg
    :target: https://github.com/jshwi/kbtogglr/actions/workflows/codeql-analysis.yml
    :alt: CodeQL
.. image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://www.python.org/downloads/release/python-380
    :alt: python3.8
.. image:: https://img.shields.io/pypi/v/kbtogglr
    :target: https://img.shields.io/pypi/v/kbtogglr
    :alt: pypi
.. image:: https://codecov.io/gh/jshwi/kbtogglr/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jshwi/kbtogglr
    :alt: codecov.io
.. image:: https://readthedocs.org/projects/kbtogglr/badge/?version=latest
    :target: https://kbtogglr.readthedocs.io/en/latest/?badge=latest
    :alt: readthedocs.org
.. image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://lbesson.mit-license.org/
    :alt: mit
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: black

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
