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

## Introducing a random bug into a project

If you don't specify a target directory or file, `py-bugger` will look at all *.py* files in the current directory before deciding where to insert a bug. If the directory is a Git repository, it will follow the rules in *.gitignore*. It will also avoid introducing bugs into test directories and virtual environments that follow familiar naming patterns.

`py-bugger` creates bugs that induce specific exceptions. In the simplest usage, `py-bugger` will choose a random bug to introduce:

```sh
$ py-bugger
Added bug.
All requested bugs inserted.
```

If your project is under version control, you can see the bug that was introduced by running `git diff`.

## Introducing a bug into a specific directory

You can target any directory:

```sh
$ py-bugger --target-dir /Users/eric/test_code/Pillow/
Added bug.
All requested bugs inserted.
```

## Introducing a bug into a specific *.py* file

And you can target a specific file:

```sh
$ py-bugger --target-file name_picker.py
Added bug.
All requested bugs inserted.
```

## Creating multiple bugs

You can create as many bugs as you like. `py-bugger` will do its best to introduce all the bugs you ask for:

```sh
$ py-bugger -n 3
Added bug.
Added bug.
Added bug.
All requested bugs inserted.
```

## Creating a specific kind of bug

Currently, `py-bugger` can create bugs that induce three kinds of exceptions: `ModuleNotFoundError`, `AttributeError`, and `IndentationError`. You can let `py-bugger` choose from these randmly, or you can ask it to create a bug that induces a specific kind of error.

Here's how to create a bug that generates a `ModuleNotFoundError`:

```sh
$ py-bugger -e ModuleNotFoundError
Added bug.
All requested bugs inserted.
```

When you run the project again, it should fail with a `ModuleNotFoundError`.

## Caveat

It's recommended to run `py-bugger` against a repository with a clean Git status. That way, if you get stuck resolving the bug that's introduced, you can either run `git diff` to see the actual bug, or restore the project to its original state. If you try to run `py-bugger` without a clean Git status you'll get a warning, which can be overridden with the `--ignore-git-status` flag.
