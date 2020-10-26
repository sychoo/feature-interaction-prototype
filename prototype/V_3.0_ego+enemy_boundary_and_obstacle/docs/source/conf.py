# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# run using Python 3.9

import os
import sys
# import sphinxcontrib.napoleon
# import numpy
# import matplotlib

# import mock

sys.path.insert(0, os.path.abspath('../../'))

# mock the imported modules
autodoc_mock_imports = ['numpy', 'matplotlib', 'seaborn']

# MOCK_MODULES = ['numpy', 'matplotlib', 'matplotlib.pyplot']
# for mod_name in MOCK_MODULES:
#     sys.modules[mod_name] = mock.Mock()


# -- Project information -----------------------------------------------------

project = 'feature-interaction'
copyright = '2020, Simon Chu'
author = 'Simon Chu'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # 'sphinxcontrib.napoleon'
    "sphinx.ext.napoleon"
    # "sphinx.ext.autodoc"

]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
