Changelog: python-bugger
===

0.1 - Proof of concept (one exception type implemented)
---

This series of releases will serve as a proof of concept for the project. If it continues to be interesting and useful to people, particularly people teaching Python, I'll continue to develop it.

I'm aiming for a stable API, but that is not guaranteed until the 1.0 release. If you have feedback about usage, please open a [discussion](https://github.com/ehmatthes/py-bugger/discussions/new/choose) or an [issue](https://github.com/ehmatthes/py-bugger/issues/new/choose).

### (Unreleased)

#### External changes

- Require `click`.
- Includes a `--num-bugs` arg.
- Modifies specified number of import nodes.
- Randomly selects which relevant node to modify.

#### Internal changes

- CLI is built on `click`, rather than `argparse`.
- Uses a random seed when `PY_BUGGER_RANDOM_SEED` env var is set, for testing.
- Utils dir, with initial `file_utils.py` module.
- Finds all .py files we can consider changing.
    - If using Git, returns all tracked .py files not related to testing.
    - If not using Git, returns all .py files not in venv, dist, build, or tests.

### 0.1.0

Initial release. Very limited implementation of:

```sh
$ py-bugger --exception-type ModuleNotFoundError
```
