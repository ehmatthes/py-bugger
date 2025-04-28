---
title: Quick Start
hide:
    - footer
---

# Quick Start

## Installation

```sh
$ pip install python-bugger
```

!!! note

    The package name is `python-bugger`, because `py-bugger` was unavailable on PyPI.

## Introducing a bug into a project

If you don't specify a target directory or file, `py-bugger` will look at all *.py* files in the current directory before deciding where to insert a bug. If the directory is a Git repository, it will follow the rules in *.gitignore*. It will also avoid introducing bugs into test directories and virtual environments that follow familiar naming patterns.

`py-bugger` creates bugs that induce specific exceptions. Here's how to create a bug that generates a `ModuleNotFoundError`:

```sh
$ py-bugger -e ModuleNotFoundError
Introducing a ModuleNotFoundError...
  Modified file.
```

When you run the project again, it should fail with a `ModuleNotFoundError`.


## Introducing a bug into a specific directory

You can target any directory:

```sh
$ py-bugger -e ModuleNotFoundError --target-dir /Users/eric/test_code/Pillow/
Introducing a ModuleNotFoundError...
  Modified file.
```

## Introducing a bug into a specific *.py* file

And you can target a specific file:

```sh
$ py-bugger -e ModuleNotFoundError --target-file name_picker.py
Introducing a ModuleNotFoundError...
  Modified file.
```

## Supported exception types

Currently, you can generate bugs that result in three exception types:

- `ModuleNotFoundError`
- `AttributeError`
- `IndentationError`

## Caveat

It's recommended to run `py-bugger` against a repository with a clean Git status. That way, if you get stuck resolving the bug that's introduced, you can either run `git diff` to see the actual bug, or restore the project to its original state.
