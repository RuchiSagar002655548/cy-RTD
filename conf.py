import os
import sys

sys.path.insert(0, os.path.abspath("."))

# Project information
project = 'cy-RTD'
author = 'RCH'
release = '0.1'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

# Paths and exclusions
templates_path = ['_templates']
exclude_patterns = []

# Options for HTML output
html_theme = 'sphinx_rtd_theme'

# Remove static paths if they're causing errors
# on_rtd = os.environ.get('READTHEDOCS') == 'True'
#if on_rtd:
 #   html_static_path = []  # Disable static paths for Read the Docs
#else:
 #   html_static_path = ['static']
