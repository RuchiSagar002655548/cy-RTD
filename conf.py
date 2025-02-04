# conf.py
import os
import sys

# Add the root directory of the project to the system path
sys.path.insert(0, os.path.abspath("."))

# -- Project Information -----------------------------------------------------
project = 'cy-RTD'
author = 'RCH'
release = '0.1'  # Version of the project (e.g., 0.1, 1.0.0)

# -- General Configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',        # Automatically include docstrings
    'sphinx.ext.napoleon',       # For Google-style or NumPy-style docstrings
    'sphinx.ext.viewcode',       # Link to source code
    'sphinx.ext.intersphinx'     # Link to other projects' docs (optional)
]

templates_path = ['_templates']   # Path to custom templates, if any
exclude_patterns = ['rtd-env/**', '**/*.dist-info/**', '**/site-packages/**']

# -- Autodoc Options ---------------------------------------------------------
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'          # You can change this to 'sphinx_rtd_theme' if preferred

# Handle output paths for both local and Read the Docs builds
if os.environ.get('READTHEDOCS'):
    # On Read the Docs, avoid specifying static paths if it's problematic
    html_static_path = []  
else:
    # Use 'static' directory for local builds
    html_static_path = ['static']
