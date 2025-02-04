import os
import sys

# Add the root directory of the project to the system path
sys.path.insert(0, os.path.abspath("."))

# Detect if we're on Read the Docs
on_rtd = os.environ.get('READTHEDOCS') == 'True'

# -- Project Information -----------------------------------------------------
project = 'cy-RTD'
author = 'RCH'
release = '0.1'

# -- General Configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',        # Automatically include docstrings
    'sphinx.ext.napoleon',       # For Google-style or NumPy-style docstrings
    'sphinx.ext.viewcode',       # Link to source code
]

templates_path = ['_templates']
exclude_patterns = ['rtd-env/**', '**/*.dist-info/**', '**/site-packages/**']

# -- Autodoc Options ---------------------------------------------------------
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'

# Handle static files depending on environment
html_static_path = [] if on_rtd else ['static']
