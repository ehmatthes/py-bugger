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

    if pb_config.target_dir:
        _validate_target_dir()

    if pb_config.target_file:
        _validate_target_file()
        
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

def _validate_target_dir():
    """Make sure a valid directory was passed.

    Check for common mistakes, then verify it is a dir.
    """
    path_target_dir = Path(pb_config.target_dir)
    if path_target_dir.is_file():
        msg = cli_messages.msg_file_not_dir(path_target_dir)
        click.echo(msg)
        sys.exit()
    elif not path_target_dir.exists():
        msg = cli_messages.msg_nonexistent_dir(path_target_dir)
        click.echo(msg)
        sys.exit()
    elif not path_target_dir.is_dir():
        msg = cli_messages.msg_not_dir(path_target_dir)
        click.echo(msg)
        sys.exit()

def _validate_target_file():
    """Make sure an appropriate file was passed.

    Check for common mistakes, then verify it is a file.
    """
    path_target_file = Path(pb_config.target_file)
    if path_target_file.is_dir():
        msg = cli_messages.msg_dir_not_file(path_target_file)
        click.echo(msg)
        sys.exit()
    elif not path_target_file.exists():
        msg = cli_messages.msg_nonexistent_file(path_target_file)
        click.echo(msg)
        sys.exit()
    elif not path_target_file.is_file():
        msg = cli_messages.msg_not_file(path_target_file)
        click.echo(msg)
        sys.exit()
    elif path_target_file.suffix != ".py":
        msg = cli_messages.msg_file_not_py(path_target_file)
        click.echo(msg)
        sys.exit()
