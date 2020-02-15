#!/usr/bin/env python3
"""Sphinx conf for KBTogglr docs"""
import os
import sys

sys.path.insert(0, os.path.abspath('..'))  # noqa
sys.path.insert(0, os.path.abspath('../kbtogglr'))  # noqa
sys.path.insert(0, os.path.abspath('../kbtogglr/src'))  # noqa
sys.path.insert(0, os.path.abspath('../kbtogglr/src/module'))  # noqa
sys.path.insert(0, os.path.abspath('../kbtogglr/src/install'))  # noqa
sys.path.insert(0, os.path.abspath('../kbtogglr/lib'))  # noqa
import kbtogglr

project = kbtogglr.__project__
# noinspection PyShadowingBuiltins
copyright = kbtogglr.__copyright__  # noqa
author = kbtogglr.__author__
release = kbtogglr.__release__
maintainer = kbtogglr.__maintainer__
email = kbtogglr.__email__
version = kbtogglr.__version__
# noinspection PyShadowingBuiltins
license = kbtogglr.__license__  # noqa

extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
    'sphinx.ext.imgmath',
    'sphinx.ext.doctest',
    'sphinx.ext.imgconverter',
    'sphinxcontrib.programoutput'
]

source_suffix = {
    '.rst': 'restructuredtext'
}
master_doc = 'index'
exclude_patterns = ['_build']
templates_path = ['_templates']
todo_include_todos = True
pygments_style = 'monokai'
autoclass_content = "both"
autodoc_member_order = 'bysource'
autodoc_default_options = {"members": None}
logo = "_static/icon.png"
add_function_parentheses = True
add_module_names = True


# # -- Options for HTML output -----------------------------------------
html_domain_indices = True
html_use_index = True
html_show_sourcelink = True
html_show_sphinx = False
html_theme = 'graphite'
html_theme_path = ['_themes']
html_static_path = ['_static']
html_logo = '_static/icon.png'
html_favicon = "_static/favicon.ico"
html_sidebars = {'**': ['globaltoc.html', 'searchbox.html']}
