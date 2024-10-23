from __future__ import annotations

import os

import sensible_bmi._version

docs_dir = os.path.dirname(__file__)

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_inline_tabs",
    # "sphinxcontrib.towncrier",
]

# templates_path = ["_templates"]

source_suffix = (".rst", ".md")

master_doc = "index"

project = "sensible_bmi"
copyright = "2024, Eric Hutton"
author = "Eric Hutton"

# The short X.Y version.
version = sensible_bmi._version.__version__
# The full version, including alpha/beta/rc tags.
release = sensible_bmi._version.__version__

language = "en"
exclude_patterns = []
pygments_style = "sphinx"
pygments_dark_style = "monokai"
modindex_common_prefix = ["sensible_bmi."]
todo_include_todos = False
html_theme = "furo"
html_title = "sensible_bmi"
# html_logo = "_static/csdms-logo.png"
html_theme_options = {
    "announcement": None,
    "source_repository": "https://github.com/mcflugen/sensible_bmi/",
    "source_branch": "main",
    "source_directory": "docs/",
    "sidebar_hide_name": True,
    "footer_icons": [
        {
            "name": "power",
            "url": "https://csdms.colorado.edu",
            "html": """
                <svg
                  stroke="currentColor"
                  fill="currentColor"
                  stroke-width="0"
                  version="1.1"
                  viewBox="0 0 16 16"
                  height="1em"
                  width="1em"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M6 0l-6 8h6l-4 8 14-10h-8l6-6z"
                  ></path>
                </svg>
                <b><i>Powered by CSDMS</i></b>
            """,
            "class": "",
        },
    ],
}
# html_static_path = ["_static"]

napoleon_numpy_docstring = True
napoleon_google_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_special_with_doc = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

# towncrier_draft_autoversion_mode = "draft"  # or: 'sphinx-release', 'sphinx-version'
# towncrier_draft_include_empty = True
# towncrier_draft_working_directory = pathlib.Path(docs_dir).parent

myst_enable_extensions = ["colon_fence"]

nbsphinx_execute = "never"
