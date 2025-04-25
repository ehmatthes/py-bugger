---
title: Contributing
hide:
    - footer
---

# Contributing

This project is still in an early phase of development, so it's a great time to jump in if you're interested. Please open or comment in an [issue](https://github.com/ehmatthes/py-bugger/issues) or a [discussion](https://github.com/ehmatthes/py-bugger/discussions) before starting any work you'd like to see merged, so we're all on the same page.

## Setting up a development environment

Clone the project, and run the tests:

```sh
$ git clone https://github.com/ehmatthes/py-bugger.git
Cloning into 'py-bugger'...
...

$ cd py-bugger-sample 
py-bugger$ uv venv .venv
py-bugger$ source .venv/bin/activate
(.venv) py-bugger$ uv pip install -e ".[dev]"
...

(.venv) py-bugger$ pytest
========== test session starts ==========
tests/e2e_tests/test_basic_behavior.py .................
tests/unit_tests/test_bug_utils.py .....
tests/unit_tests/test_file_utils.py ...
========== 25 passed in 3.29s ==========
```

## Development work

There are two good approaches to development work. The first focuses on running `py-bugger` against a single .py file; the second focuses on running against a larger project with multiple .py files, nested in a more complex file structure.

### Running `py-bugger` against a single .py file

Make a directory somewhere on your system, outside the `py-bugger` directory. Add a single .py file, and make an initial Git commit. Install `py-bugger` in editable mode, with a command like this: `uv pip install -e /path/to/py-bugger/`.

The single file should be a minimal file that lets you introduce the kind of bug you're trying to create. For example if you want to focus on `IndentationError`, make a file of just a few lines, with an indented block. Now you can run `py-bugger`, see that it generates the expected error type, and run `git checkout .` to restore the .py file.

### Running `py-bugger` against a larger project

Once you have `py-bugger` working against a single .py file, you'll want to run it against a larger project as well. I've been using Pillow in development work, because it's a mature project with lots of nested .py files, and it has a solid test suite that runs in less than a minute. Whatever project you choose, make sure it has a well-developed test suite. Install `py-bugger` in editable mode, run it against the project, and then make sure the tests fail in the expected way due to the bug that was introduced.