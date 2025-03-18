import argparse


def parse_cli_args():
    """Parse all options for the CLI."""
    parser = argparse.ArgumentParser(
        description="Practice debugging, by intentionally introducing bugs into an existing codebase."
    )

    parser.add_argument(
        "-e",
        "--exception-type",
        type=str,
        help="What kind of exception to induce.",
    )

    # The --target-dir arg is useful for testing, and may be useful for end users as well.
    parser.add_argument(
        "--target-dir",
        type=str,
        help="What code directory to target. (Be careful when using this arg!)"
    )

    args = parser.parse_args()

    return args
