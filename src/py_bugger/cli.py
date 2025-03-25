import sys
from pathlib import Path
import os

import click

from py_bugger import py_bugger
from py_bugger import cli_messages


@click.command()
@click.option(
    "--exception-type",
    "-e",
    type=str,
    help="What kind of exception to induce.",
)
@click.option(
    "--target-dir",
    type=str,
    help="What code directory to target. (Be careful when using this arg!)",
)
@click.option(
    "--num-bugs",
    "-n",
    type=int,
    default=1,
    help="How many bugs to introduce.",
)
def cli(exception_type, target_dir, num_bugs):
    """Practice debugging, by intentionally introducing bugs into an existing codebase."""
    if not exception_type:
        click.echo(cli_messages.msg_bare_call)
        sys.exit()

    # Make sure target_dir is a Path object, and set to cwd if empty.
    target_dir = _set_target_dir(target_dir)

    py_bugger.main(exception_type, target_dir, num_bugs)


# --- Helper functions (move to a cli/utils.py module) ---


def _set_target_dir(target_dir):
    """Set an appropriate target directory."""
    if target_dir:
        return Path(target_dir)
    else:
        return Path(os.getcwd())
