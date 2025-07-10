Changelog: python-bugger
===

0.5 - Support multiple exception types in one call

Previously, any single run of `py-bugger` could only create bugs that induce one kind of exception. In the 0.5 series, a variety of bugs can be introduced in a single call.

### 0.5.0

#### External changes

- When no `-e` arg is passed, generates a random sequence of bugs to induce.
- Docs updated to reflect current usage.

#### Internal changes

- Main loop works from a list of bugs to introduce, rather than ranging over `num_bugs`.
- Reorders `requested_bugs` so CST-based parsing happens before regex-based parsing. Avoids writing syntax-related bugs before parsing nodes.
- Started integration tests that should take the place of many current e2e tests. Calls `py_bugger.main()` directly, and checks `requested_bugs` and `modfications`.
- `Modification` objects record the exception type that's induced.

0.4 - Git status checks
---

Looks for a clean Git status before introducing bugs.

### 0.4.1

#### External changes

- The `--exception-type` argument is now optional. When it's omitted, one of the supported exception types is chosen randomly.
- Passing `--num-args` still works, but each bug induces the same kind of exception.
- If there's a typo in the value for `--exception-type`, a suggestion is made. Users still need to revise their command, it does not prompt to use the suggested value at this point.
- Fixes a bug where running py-bugger from a directory under version control, against a target directory that's also under version control, runs Git commands against the first directory instead of the target.

#### Internal changes

- Uses `SUPPORTED_EXCEPTION_TYPES` from `py_bugger.cli.config` anywhere a list of supported exception types is needed.
- All handling of `--num-args` takes place in the main py_bugger.py file.
- Tracks each bug that's introduced, so each node or line can't be modified more than once. There's a new `Modification` model that's used to track each modification that's made to the user's code. This also simplifies tracking the number of bugs, which can always be determined from `len(modifications)`.
- Some light ongoing refactoring work has been done through this point release.

### 0.4.0

#### External changes

- Checks Git status before introducing bugs.
- Allows overriding Git checks with `--ignore-git-status`.

#### Internal changes

- Moving `py_bugger` import closer to where it's needed speeds up tests.


0.3 - Multiple exception types targeted
---

Can request more than one type of exception to be induced.

### 0.3.6

#### External changes

- Includes validation for --target-dir and --target-file args.

### 0.3.5

#### External changes

- Removes else, elif, case, except and finally from targets for IndentationError for now.

#### Internal changes

- Added a release script.
- Partial implementation of a test for handling tabs correctly.

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
