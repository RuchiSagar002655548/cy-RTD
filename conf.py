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
    'sphinx.ext.intersphinx'     # Link to other projects' docs (optional)
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

# Handle static paths for both local and RTD builds
if on_rtd:
    html_static_path = []  # Disable static files on Read the Docs to avoid errors
else:
    html_static_path = ['static']  # Use the 'static' directory locally

# Handle output paths for Read the Docs
if on_rtd:
    html_output_dir = os.environ.get('READTHEDOCS_OUTPUT', '_build/html')
