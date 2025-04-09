"""Utility functions for the CLI.

If this grows into groups of utilities, move to a cli/utils/ dir, with more specific
filenames.
"""

import os
import sys
from pathlib import Path

import click

from py_bugger.cli import cli_messages
from py_bugger.cli.config import pb_config


def validate_config():
    """Make sure the CLI options are valid."""
    if not pb_config.exception_type:
        click.echo(cli_messages.msg_exception_type_required)
        sys.exit()

    if pb_config.target_dir and pb_config.target_file:
        click.echo(cli_messages.msg_target_file_dir)
        sys.exit()

    _update_options()


# --- Helper functions ___


def _update_options():
    """Make sure options are ready to use."""
    # Set an appropriate target directory.
    if pb_config.target_dir:
        pb_config.target_dir = Path(pb_config.target_dir)
    else:
        pb_config.target_dir = Path(os.getcwd())

    # Make sure target_file is a Path.
    if pb_config.target_file:
        pb_config.target_file = Path(pb_config.target_file)
