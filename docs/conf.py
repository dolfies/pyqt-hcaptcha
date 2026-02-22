# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import re
import sys

sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PyQtHCaptcha'
copyright = '2026, Dolfies'
author = 'Dolfies'

version = ""
with open("../PyQtHCaptcha/__init__.py") as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)  # type: ignore

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
]

# Mock heavy Qt imports so docs build without a Qt installation
autodoc_mock_imports = ['PyQt6']

autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autodoc_typehints_description_target = 'documented'

napoleon_use_param = True
napoleon_use_rtype = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_title = 'PyQtHCaptcha'

html_theme_options = {
    'sidebar_hide_name': False,
}

# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# PyQt6 has no intersphinx inventory; suppress unresolvable cross-references
nitpick_ignore = [
    ('py:class', 'PyQt6.QtWebEngineCore.QWebEnginePage'),
    ('py:class', 'PyQt6.QtWebEngineWidgets.QWebEngineView'),
    ('py:class', 'pyqtBoundSignal'),
]
