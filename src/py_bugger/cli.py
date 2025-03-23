import click

import py_bugger


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
    help="What code directory to target. (Be careful when using this arg!)"
)
def cli(exception_type, target_dir):
    """CLI entrypoint for python-bugger."""
    if not exception_type:
        click.echo(cli_messages.msg_bare_call)

    py_bugger.main(exception_type, target_dir)




# def parse_cli_args():
#     """Parse all options for the CLI."""
#     parser = argparse.ArgumentParser(
#         description="Practice debugging, by intentionally introducing bugs into an existing codebase."
#     )

#     parser.add_argument(
#         "-e",
#         "--exception-type",
#         type=str,
#         help="What kind of exception to induce.",
#     )

#     # The --target-dir arg is useful for testing, and may be useful for end users as well.
#     parser.add_argument(
#         "--target-dir",
#         type=str,
#         help="What code directory to target. (Be careful when using this arg!)"
#     )

#     args = parser.parse_args()

#     return args
