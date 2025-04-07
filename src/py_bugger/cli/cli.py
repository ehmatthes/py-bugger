from pathlib import Path

import click

from py_bugger import py_bugger
from py_bugger.cli import cli_utils


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
    cli_utils.validate_cli(exception_type, target_dir, target_file)

    # Make sure we're passing appropriate Path objects.
    target_dir = cli_utils.set_target_dir(target_dir)
    if target_file:
        target_file = Path(target_file)

    py_bugger.main(exception_type, target_dir, target_file, num_bugs)
