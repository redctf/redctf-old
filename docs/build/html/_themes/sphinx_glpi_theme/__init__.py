"""Sphinx GLPI theme.
From https://github.com/rtfd/sphinx_rtd_theme.
"""
import os

__version__ = '0.3'
__version_full__ = __version__

def get_html_themes_path():
    """Return list of sphinx themes."""
    here = os.path.abspath(os.path.dirname(__file__))
    return [here]
