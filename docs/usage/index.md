---
title: Usage
hide:
    - footer
---

# Usage

This page covers the full usage options for `py-bugger`. If you haven't already read the [Quick Start](../quick_start/index.md) page, it's best to start there.

Here's the output of `py-bugger --help`, which summarizes all usage options:

```sh
Usage: py-bugger [OPTIONS]

  Practice debugging, by intentionally introducing bugs into an existing
  codebase.

Options:
  -e, --exception-type TEXT  What kind of exception to induce:
                             ModuleNotFoundError, AttributeError, or
                             IndentationError
  --target-dir TEXT          What code directory to target. (Be careful when
                             using this arg!)
  --target-file TEXT         Target a single .py file.
  --target-lines TEXT        Target a specific block of lines. A single
                             integer, or a range.
  -n, --num-bugs INTEGER     How many bugs to introduce.
  --ignore-git-status        Don't check Git status before inserting bugs.
  -v, --verbose              Enable verbose output.
  --help                     Show this message and exit.
```

## Targeting specific lines

You can target a specific line or block of lines in a file:

```sh
$ py-bugger --target-file dog.py --target-lines 15
$ py-bugger --target-file dog.py --target-lines 15-20
```

The `--target-lines` argument only works if you're also passing a value for `--target-file`.

## Introducing multiple bugs of specific types

Currently, it's not possible to specify more than one exception type in a single `py-bugger` call. At the moment, you can either let `py-bugger` choose which kind of bug to introduce, or you can request a specific exception to induce.

If you need to introduce several specific bugs, but not choose randomly from all possible bugs, you may have luck running `py-bugger` multiple times with different exception types:

```sh
$ py-bugger -e ModuleNotFoundError
$ py-bugger -e IndentationError -n 2
```

This can fail if a bug introduces a syntax error which prevents `py-bugger` from parsing your codebase. Support for specifying multiple exception types should be added shortly. If this kind of usage is important to you, please consider opening an [issue](https://github.com/ehmatthes/py-bugger/issues) or [discussion](https://github.com/ehmatthes/py-bugger/discussions), and I'll prioritize support for this.

## A note about speed

Some bugs are easier to create than others. For example you can induce an `IndentationError` without closely examining the code. Other bugs take more work; to induce an `AttributeError`, you need to examine the code much more closely. Depending on the size of the codebase you're working with, you might see some very quick runs and some very slow runs. This is expected behavior.
