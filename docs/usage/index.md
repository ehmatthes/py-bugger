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
  -n, --num-bugs INTEGER     How many bugs to introduce.
  --help                     Show this message and exit.
```

## Introducing multiple bugs

Currently, you can create multiple bugs that target any of the supported exception types. For example, this command will try to introduce three bugs that each induce an `IndentationError`:

```sh
$ py-bugger -e IndentationError --n 3
```

## Introducing mulitple bugs of different types

Currently, it's not possible to specify more than one exception type in a single `py-bugger` call. You may have luck running `py-bugger` multiple times, with different exception types:

```sh
$ py-bugger -e IndentationError -n 2
$ py-bugger -e ModuleNotFoundError
```

## A note about speed

Some bugs are easier to create than others. For example you can induce an `IndentationError` without closely examining the code. Other bugs take more work; to induce an `AttributeError`, you need to examine the code much more closely. Depending on the size of the codebase you're working with, you might see some very quick runs and some very slow runs. This is expected behavior.
