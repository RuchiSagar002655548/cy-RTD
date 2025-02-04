# conf.py

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
exclude_patterns = []            # Exclude patterns for files or directories

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'          # You can change this to 'sphinx_rtd_theme' if preferred
html_static_path = ['_static']    # Static files such as images, CSS, etc.
