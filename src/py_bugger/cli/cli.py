import sys
from pathlib import Path
import os

import click

from py_bugger import py_bugger
from py_bugger.cli import cli_messages


@click.command()
@click.option(
    "--exception-type",
    "-e",
    type=str,
    help="What kind of exception to induce: ModuleNotFoundError, AttributeError, or IndentationError",
)
@click.option(
    "--target-dir",
    type=str,
    help="What code directory to target. (Be careful when using this arg!)",
)
@click.option(
    "--target-file",
    type=str,
    help="Target a single .py file.",
)
@click.option(
    "--num-bugs",
    "-n",
    type=int,
    default=1,
    help="How many bugs to introduce.",
)
def cli(exception_type, target_dir, target_file, num_bugs):
    """Practice debugging, by intentionally introducing bugs into an existing codebase."""
    _validate_cli(exception_type, target_dir, target_file)

    # Make sure we're passing appropriate Path objects.
    target_dir = _set_target_dir(target_dir)
    if target_file:
        target_file = Path(target_file)

    py_bugger.main(exception_type, target_dir, target_file, num_bugs)


# --- Helper functions (move to a cli/utils.py module) ---

def _validate_cli(exception_type, target_dir, target_file):
    """Make sure we have a valid call."""
    if not exception_type:
        click.echo(cli_messages.msg_exception_type_required)
        sys.exit()

    if target_dir and target_file:
        click.echo(cli_messages.msg_target_file_dir)
        sys.exit()


def _set_target_dir(target_dir):
    """Set an appropriate target directory."""
    if target_dir:
        return Path(target_dir)
    else:
        return Path(os.getcwd())
