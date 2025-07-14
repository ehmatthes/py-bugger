import click

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
    "--target-lines",
    type=str,
    help="Target a specific block of lines. A single integer, or a range.",
)
@click.option(
    "--num-bugs",
    "-n",
    type=int,
    default=1,
    help="How many bugs to introduce.",
)
@click.option(
    "--ignore-git-status",
    is_flag=True,
    help="Don't check Git status before inserting bugs.",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output.",
)
def cli(**kwargs):
    """Practice debugging, by intentionally introducing bugs into an existing codebase."""
    # Update pb_config using options passed through CLI call.
    pb_config.__dict__.update(kwargs)
    cli_utils.validate_config()

    # Importing py_bugger here cuts test time significantly, as these resources are not
    # loaded for many calls. (6.7s -> 5.4s, for 20% speedup, 6/10/25.)
    from py_bugger import py_bugger

    py_bugger.main()
