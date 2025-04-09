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


def set_target_dir(target_dir):
    """Set an appropriate target directory."""
    if target_dir:
        return Path(target_dir)
    else:
        return Path(os.getcwd())
