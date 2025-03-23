Changelog: python-bugger
===

0.1 - Proof of concept (one exception type implemented)
---

This series of releases will serve as a proof of concept for the project. If it continues to be interesting and useful to people, particularly people teaching Python, I'll continue to develop it.

I'm aiming for a stable API, but that is not guaranteed until the 1.0 release. If you have feedback about usage, please open a [discussion](https://github.com/ehmatthes/py-bugger/discussions/new/choose) or an [issue](https://github.com/ehmatthes/py-bugger/issues/new/choose).

### (Unreleased)

#### External changes

- Require `click`.

#### Internal changes

- CLI is built on `click`, rather than `argparse`.

### 0.1.0

Initial release. Very limited implementation of:

```sh
$ py-bugger --exception-type ModuleNotFoundError
```