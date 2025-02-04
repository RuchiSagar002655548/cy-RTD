import os
import sys

# Add the root directory of the project to the system path
sys.path.insert(0, os.path.abspath("."))

# Detect if the build is happening on Read the Docs
on_rtd = os.environ.get('READTHEDOCS') == 'True'

# -- Project Information --
project = 'cy-RTD'
author = 'RCH'
release = '0.1'

# -- General Configuration --
extensions = [
    'sphinx.ext.autodoc',        # Automatically include docstrings
    'sphinx.ext.napoleon',       # For Google-style or NumPy-style docstrings
    'sphinx.ext.viewcode',       # Link to source code
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output --
html_theme = 'sphinx_rtd_theme'

# Handle static files: disable on RTD if it raises warnings
html_static_path = [] if on_rtd else ['static']

