"""Utility functions for the CLI.

If this grows into groups of utilities, move to a cli/utils/ dir, with more specific
filenames.
"""

import os
import sys
from pathlib import Path
import subprocess
import shlex
import shutil
import difflib

import click

from py_bugger.cli import cli_messages
from py_bugger.cli.config import pb_config
from py_bugger.cli.config import SUPPORTED_EXCEPTION_TYPES


def validate_config():
    """Make sure the CLI options are valid."""

    if pb_config.target_dir and pb_config.target_file:
        click.echo(cli_messages.msg_target_file_dir)
        sys.exit()

    _validate_exception_type()

    if pb_config.target_dir:
        _validate_target_dir()

    if pb_config.target_file:
        _validate_target_file()

    if pb_config.target_lines:
        _validate_target_lines()

    # Update all options before running Git status checks. Info like target_dir
    # is used for those checks.
    _update_options()

    _validate_git_status()


# --- Helper functions ___


def _update_options():
    """Make sure options are ready to use."""
    # Set an appropriate target directory.
    if pb_config.target_dir:
        pb_config.target_dir = Path(pb_config.target_dir)
    else:
        pb_config.target_dir = Path(os.getcwd())


def _validate_exception_type():
    """Make sure the -e arg provided is supported."""
    if not pb_config.exception_type:
        return

    if pb_config.exception_type in SUPPORTED_EXCEPTION_TYPES:
        return

    # Check for typos.
    matches = difflib.get_close_matches(
        pb_config.exception_type, SUPPORTED_EXCEPTION_TYPES, n=1
    )
    if matches:
        msg = cli_messages.msg_apparent_typo(pb_config.exception_type, matches[0])
        click.echo(msg)
        sys.exit()

    # Invalid or unsupported exception type.
    msg = cli_messages.msg_unsupported_exception_type(pb_config.exception_type)
    click.echo(msg)
    sys.exit()


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

    # It's valid, set it to a Path.
    pb_config.target_file = path_target_file

def _validate_target_lines():
    """Make sure an appropriate block of lines was passed."""
    # You can only pass target lines if you're also passing a target file.
    if not pb_config.target_file:
        click.echo(cli_messages.msg_target_lines_no_target_file)
        sys.exit()

    # Handle a single target line.
    if "-" not in pb_config.target_lines:
        target_line = int(pb_config.target_lines.strip())

        # Make sure this line is in the target file.
        lines = pb_config.target_file.read_text().splitlines()
        if target_line > len(lines):
            msg = cli_messages.msg_invalid_target_line(target_line, pb_config.target_file, len(lines))
            click.echo(msg)
            sys.exit()

        # Wrap target_line in a list, and return.
        pb_config.target_lines = [target_line]
        return

    # Handle a block of lines.
    start, end = pb_config.target_lines.strip().split("-")
    start, end = int(start), int(end)

    # Make sure end line is in the target file.
    lines = pb_config.target_file.read_text().splitlines()
    if end > len(lines):
        msg = cli_messages.msg_invalid_target_lines(end, pb_config.target_file, len(lines))
        click.echo(msg)
        sys.exit()

    pb_config.target_lines = list(range(start, end+1))


def _validate_git_status():
    """Look for a clean Git status before introducing bugs."""
    if pb_config.ignore_git_status:
        return

    _check_git_available()
    _check_git_status()


def _check_git_available():
    """Quit with appropriate message if Git not available."""
    if not shutil.which("git"):
        click.echo(cli_messages.msg_git_not_available)
        sys.exit()


def _check_git_status():
    """Make sure we're starting with a clean git status."""
    if pb_config.target_file:
        git_dir = pb_config.target_file.parent
    else:
        git_dir = pb_config.target_dir

    cmd = "git status --porcelain"
    cmd_parts = shlex.split(cmd)
    output = subprocess.run(cmd_parts, cwd=git_dir, capture_output=True, text=True)

    if "fatal: not a git repository" in output.stderr:
        msg = cli_messages.msg_git_not_used(pb_config)
        click.echo(msg)
        sys.exit()

    # `git status --porcelain` has no output when the status is clean.
    if output.stdout or output.stderr:
        msg = cli_messages.msg_unclean_git_status
        click.echo(msg)
        sys.exit()
