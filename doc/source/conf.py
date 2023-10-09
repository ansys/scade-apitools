"""Sphinx documentation configuration file."""
from datetime import datetime
import os
import sys

from ansys_sphinx_theme import ansys_favicon, get_version_match
from ansys_sphinx_theme import pyansys_logo_black as logo
from sphinx.highlighting import lexers

sys.path.append('.')
from _lexers.swan import SwanLexer

# allow custom extensions
sys.path.append(os.path.abspath("./_ext"))

# Project information
project = "ansys-scade-apitools"
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "ANSYS, Inc."
release = version = "0.3.0"

# Select desired logo, theme, and declare the html title
html_logo = logo
html_theme = "ansys_sphinx_theme"
html_short_title = html_title = "pyscade-apitools"

# multi-version documentation
cname = os.getenv("DOCUMENTATION_CNAME", "apitools.scade.docs.pyansys.com")
"""The canonical name of the webpage hosting the documentation."""

# specify the location of your github repo
html_theme_options = {
    "github_url": "https://github.com/ansys/scade-apitools",
    "show_prev_next": False,
    "show_breadcrumbs": True,
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
    ],
    "switcher": {
        "json_url": f"https://{cname}/versions.json",
        "version_match": get_version_match(version),
    },
    "check_switcher": False,
}

# Sphinx extensions
extensions = [
    "sphinx.ext.autodoc",
    # "sphinx.ext.autodoc.typehints",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    # JH "numpydoc",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    # "sphinx_gallery.gen_gallery",
    # apitools examples
    'ex',
]

# Print the type annotations from the signature in the description only
autodoc_typehints = 'description'
# When the documentation is run on Linux systems
autodoc_mock_imports = ['scade', 'scade_env', '_scade_api']
# Purpose of this option?
add_module_names = False

# autoclass_content: keep default
# autoclass_content = 'both'
# autodoc_class_signature: can't be used with enums
# autodoc_class_signature = 'separated'

# sphinx_gallery_conf = {
#     "examples_dirs": "../examples",   # path to your example scripts
#     "gallery_dirs": "examples",  # path where the gallery generated output will be saved
# }

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/dev", None),
    # kept here as an example
    # "scipy": ("https://docs.scipy.org/doc/scipy/reference", None),
    # "numpy": ("https://numpy.org/devdocs", None),
    # "matplotlib": ("https://matplotlib.org/stable", None),
    # "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
    # "pyvista": ("https://docs.pyvista.org/", None),
    # "grpc": ("https://grpc.github.io/grpc/python/", None),
}

# numpydoc configuration
numpydoc_show_class_members = False
numpydoc_xref_param_type = True

# Consider enabling numpydoc validation. See:
# https://numpydoc.readthedocs.io/en/latest/validation.html#
numpydoc_validate = True
numpydoc_validation_checks = {
    "GL06",  # Found unknown section
    "GL07",  # Sections are in the wrong order.
    "GL08",  # The object does not have a docstring
    "GL09",  # Deprecation warning should precede extended summary
    "GL10",  # reST directives {directives} must be followed by two colons
    "SS01",  # No summary found
    "SS02",  # Summary does not start with a capital letter
    # "SS03", # Summary does not end with a period
    "SS04",  # Summary contains heading whitespaces
    # "SS05", # Summary must start with infinitive verb, not third person
    "RT02",  # The first line of the Returns section should contain only the
    # type, unless multiple values are being returned"
}

# lexer for Scade
lexers['swan'] = SwanLexer(startinline=True)

# Favicon
html_favicon = ansys_favicon

# static path
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"
