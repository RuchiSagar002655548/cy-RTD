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
    'sphinx.ext.viewcode',
]
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'          # You can change this to 'sphinx_rtd_theme' if preferred
html_static_path = ['static'] 
