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

Here's an example, using *simple_indent.py* from the *tests/sample_code/sample_scripts/* [directory](https://github.com/ehmatthes/py-bugger/tree/main/tests/sample_code/sample_scripts):

```sh
$ mkdir pb-simple-test && cd pb-simple-test 
pb-simple-test$ cp ~/projects/py-bugger/tests/sample_code/sample_scripts/simple_indent.py simple_indent.py
pb-simple-test$ ls
simple_indent.py
pb-simple-test$ nano .gitignore
pb-simple-test$ git init
Initialized empty Git repository in pb-simple-test/.git/
pb-simple-test$ git add .
pb-simple-test$ git commit -am "Initial state."
pb-simple-test$ uv venv .venv
pb-simple-test$ source .venv/bin/activate
(.venv) pb-simple-test$ uv pip install -e ~/projects/py-bugger/
(.venv) pb-simple-test$ python simple_indent.py 
1
2
3

(.venv) pb-simple-test$ py-bugger -e IndentationError
Added bug to: simple_indent.py
All requested bugs inserted.

(.venv) pb-simple-test$ python simple_indent.py 
  File "/Users/eric/test_codepb-simple-test/simple_indent.py", line 1
    for num in [1, 2, 3]:
IndentationError: unexpected indent

(.venv) pb-simple-test$ git checkout .
(.venv) pb-simple-test$ python simple_indent.py 
1
2
3
```

### Running `py-bugger` against a larger project

Once you have `py-bugger` working against a single .py file, you'll want to run it against a larger project as well. I've been using Pillow in development work, because it's a mature project with lots of nested .py files, and it has a solid test suite that runs in less than a minute. Whatever project you choose, make sure it has a well-developed test suite. Install `py-bugger` in editable mode, run it against the project, and then make sure the tests fail in the expected way due to the bug that was introduced.