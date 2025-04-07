"""Utility functions for the CLI.

If this grows into groups of utilities, move to a cli/utils/ dir, with more specific
filenames.
"""

import os
import sys
from pathlib import Path

import click

from py_bugger.cli import cli_messages


def validate_cli(exception_type, target_dir, target_file):
    """Make sure we have a valid call."""
    if not exception_type:
        click.echo(cli_messages.msg_exception_type_required)
        sys.exit()

    if target_dir and target_file:
        click.echo(cli_messages.msg_target_file_dir)
        sys.exit()


def set_target_dir(target_dir):
    """Set an appropriate target directory."""
    if target_dir:
        return Path(target_dir)
    else:
        return Path(os.getcwd())
