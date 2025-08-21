# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
import pathlib
#sys.path.insert(0, os.path.abspath('/home/teja/OneDrive/Research/Dev/pyMAPPINGS/'))
DOCS = pathlib.Path(__file__).resolve().parent
ROOT = DOCS.parent

# If you use a src/ layout, this picks it up automatically
SRC = ROOT / "src"
sys.path.insert(0, str(SRC if SRC.exists() else ROOT))
project = 'pyMAPPINGS'
copyright = '2025, Teja Teppala'
author = 'Teja Teppala'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    "sphinx.ext.autosummary",
    'sphinx.ext.napoleon',      # for Google/NumPy-style docstrings
    'sphinx.ext.viewcode',
]


templates_path = ['_templates']
exclude_patterns = []

autosummary_generate = True           # build stub pages from docstrings
autodoc_typehints = "description"     # cleaner signature docs
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = 'sphinx_rtd_theme'
# html_theme = 'alabaster'
html_static_path = ['_static']
