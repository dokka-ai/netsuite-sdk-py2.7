# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
from __future__ import absolute_import
import os
import sys
# sys.path.insert(0, os.path.abspath('.'))

sys.path.insert(0, os.path.abspath(u'..'))


# -- Project information -----------------------------------------------------

project = u'netsuite-sdk-py'
copyright = u'2019, Sivaramakrishnan Narayanan, Lothar Spiegel'
author = u'Sivaramakrishnan Narayanan, Lothar Spiegel'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    u'sphinx.ext.autodoc',
    u'sphinx.ext.viewcode',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = [u'_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [u'_build', u'Thumbs.db', u'.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = u'classic'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = [u'_static']
