from pathlib import Path

import click

from py_bugger import py_bugger
from py_bugger.cli import cli_utils
from py_bugger.cli.config import pb_config


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
    pb_config.exception_type = exception_type
    pb_config.target_dir = target_dir
    pb_config.target_file = target_file
    pb_config.num_bugs = num_bugs

    cli_utils.validate_config()

    # Make sure we're passing appropriate Path objects.
    pb_config.target_dir = cli_utils.set_target_dir(pb_config.target_dir)
    if pb_config.target_file:
        pb_config.target_file = Path(pb_config.target_file)

    py_bugger.main()
