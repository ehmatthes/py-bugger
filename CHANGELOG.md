Changelog: python-bugger
===

0.3 - Multiple exception types targeted

Can request more than one type of exception to be induced.

### 0.3.4

#### External changes

- Fixes a bug where the last trailing newline was not written back to the file after introducing bugs that cause an `IndentationError`.

#### Internal changes

- Adds thorough tests for handling trailing newlines when modifying files.

### 0.3.3

#### External changes

- Added a `--verbose` (`-v`) flag. Only shows where bugs were added when this flag is present.

#### Internal changes

- The `pb_config` object is imported directly into *buggers.py*, and does not need to be passed to each bugger function.

### 0.3.2

#### External changes

- Does not modify files in directories named `Tests/`.
- Moved docs to Read the Docs.

#### Internal changes

- Set up CI.
- Move CLI code to a cli/ dir.
- Move buggers.py out of utils/.
- Make a cli_utils.py module.
- Use a `config` object for CLI options.
- Simpler parsing of CLI options.
- Simpler approach to getting `py_files` in `main()`.
- Issue template for bug reports.
- Move helper functions from buggers.py to appropriate utility modules.

### 0.3.1

#### External changes

- Wider variety of bugs generated to induce requested exception type.
    - Greater variety of typos.
    - Greater variety in placement of bugs.
- Supports `-e IndentationError`.

#### Internal changes

- The `developer_resources/` dir contains sample nodes.
- Uses a generic `NodeCollector` class.
- Utility functions for generating bugs, ie `utils/bug_utils.make_typo()`.
- End to end tests are less specific, so more resilient to changes in bugmaking algos, while still ensuring the requested exception type is induced.
- Helper function to get all nodes in a file, to support development work.
- Use `random.sample()` (no replacement) rather than `random.choices()` (uses replacement) when selecting which nodes to modify.

### 0.3.0

#### External changes

- Support for `--exception-type AttributeError`.


0.2 - Much wider range of bugs possible
---

Still only results in a `ModuleNotFoundError`, but creates a much wider range of bugs to induce that error. Also, much better overall structure for continued development.

### 0.2.1

#### External changes

- Filters out .py files from dirs named `test_code/`.

### 0.2.0

#### External changes

- Require `click`.
- Includes a `--num-bugs` arg.
- Modifies specified number of import nodes.
- Randomly selects which relevant node to modify.
- Reports level of success.
- Supports `--target-file` arg.
- Better messaging when not including `--exception-type`.

#### Internal changes

- CLI is built on `click`, rather than `argparse`.
- Uses a random seed when `PY_BUGGER_RANDOM_SEED` env var is set, for testing.
- Utils dir, with initial `file_utils.py` module.
- Finds all .py files we can consider changing.
    - If using Git, returns all tracked .py files not related to testing.
    - If not using Git, returns all .py files not in venv, dist, build, or tests.
- Catches `TypeError` if unable to make desired change; we can focus on these kinds of changes as the project evolves.


0.1 - Proof of concept (one exception type implemented)
---

This series of releases will serve as a proof of concept for the project. If it continues to be interesting and useful to people, particularly people teaching Python, I'll continue to develop it.

I'm aiming for a stable API, but that is not guaranteed until the 1.0 release. If you have feedback about usage, please open a [discussion](https://github.com/ehmatthes/py-bugger/discussions/new/choose) or an [issue](https://github.com/ehmatthes/py-bugger/issues/new/choose).

### 0.1.0

Initial release. Very limited implementation of:

```sh
$ py-bugger --exception-type ModuleNotFoundError
```
