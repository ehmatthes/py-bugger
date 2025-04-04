Changelog: python-bugger
===

0.3 - Multiple exception types targeted

Can request more than one type of exception to be induced.

### 0.3.2

#### External changes

- NA

#### Internal changes

- Set up CI.

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
