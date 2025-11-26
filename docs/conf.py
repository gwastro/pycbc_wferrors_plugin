# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pycbc_wferrors_plugin'

import datetime
year = datetime.datetime.now().year
copyright = f'{year}, The PyCBC Team'
# copyright = '2025, Sumit Kumar and Max Melching and Frank Ohme'

author = 'Sumit Kumar and Max Melching and Frank Ohme'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.todo',  # includes todos
    'sphinx.ext.viewcode',  # syntax highlighting
    'sphinx.ext.autodoc',  # includes documentation from docstrings
    'sphinx.ext.napoleon',  # support other docstring formats
    'sphinx.ext.mathjax',
    'sphinx.ext.autosectionlabel',  # Enables :ref:`section name`
    'sphinx.ext.intersphinx',
    'm2r2',  # including markdown files
    # 'sphinx_mdinclude',  # including markdown files -> then comment m2r2 -> seems to work much better -> but not compatible with nbsphinx...
    'nbsphinx',
    'nbsphinx_link'
]


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_theme_options = {
    'logo_only': False,
    # 'display_version': True,
    # -- Options for TOC sidebar
    'collapse_navigation': False,  # Makes navigation expandable
    'sticky_navigation': True,
    'navigation_depth': 4,
    'titles_only': False
}

