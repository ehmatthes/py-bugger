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

$ cd py-bugger 
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

Here's how to run py-bugger against Pillow, and verify that it worked as expected:

```sh
$ git clone https://github.com/python-pillow/Pillow.git pb-pillow
$ cd pb-pillow
pb-pillow$ uv venv .venv
pb-pillow$ source .venv/bin/activate
(.venv) /pb-pillow$ uv pip install -e ".[tests]"
(.venv) /pb-pillow$ pytest
...
========== 4692 passed, 259 skipped, 3 xfailed in 46.65s ==========

(.venv) /pb-pillow$ uv pip install -e ~/projects/py-bugger
(.venv) /pb-pillow$ py-bugger -e AttributeError
Added bug to: src/PIL/TiffImagePlugin.py
All requested bugs inserted.
(.venv) /pb-pillow$ pytest -qx
...
E   AttributeError: module 'PIL.TiffTags' has no attribute 'LONmG8'. Did you mean: 'LONG8'?
========== short test summary info ==========
ERROR Tests/test_file_libtiff.py - AttributeError: module 'PIL.TiffTags' has no attribute 'LONmG8'. Did you mean: 'LONG8'?
!!!!!!!!!! stopping after 1 failures !!!!!!!!!!
1 error in 0.33s
```

!!! note

    When you install the project you want to test against, make sure you install it in editable mode. I've made the mistake of installing Pillow without the `-e` flag, and the tests keep passing no matter how many bugs I add.

## Overall logic

It's helpful to get a quick sense of how the project works.

### `src/py_bugger/cli/cli.py`

The main public interface is defined in `cli.py`. The `cli()` function updates the `pb_config` object based on the current CLI args. These args are then validated, and the `main()` function is called.

### `src/py_bugger/py_bugger.py`

The `main()` function in `py_bugger.py` collects the `py_files` that we can consider modifying. It then calls out to "bugger" functions that inspect the target code, identifying all the ways we could modify it to introduce the requested kind of bug. The actual bug that's introduced is chosen randomly on each run. After introducing bugs, a `success_msg` is generated showing whether the requested bugs were inserted.

### Notes

- This is the ideal take. Currently, we're not identifying all possible ways any given bug could be introduced. Each bug that's supported is implemented in a way that we should see a significant variety of bugs generated in a project of moderate complexity.
- The initial internal structure has not been fully refactored yet, because there's some behavior yet to refine. To be specific, questions about supporting multiple types of bugs in one call, and supporting logical errors will impact internal structure.

## Parsing code

To introduce bugs, `py-bugger` needs to inspect all the code in the target .py file, or the appropriate set of .py files in a project. For most bugs, `py-bugger` uses a *Concrete Syntax Tree* (CST) to do this. When you convert Python code to an *Abstract Syntax Tree* (AST), it loses all comments and non-significant whitespace. We can't really use an AST, because we need to preserve the original comments and whitespace. A CST is like an AST, with comments and nons-significant whitespace included.

Consider trying to induce an `AttributeError`. We want to find all attributes in a set of .py files. The CST is perfect for that. But if we want to find all indented lines, it can be simpler (and much faster) to just parse all the lines in all the files, and look for any leading whitespace.

As the project evolves, most work will probably be done using the CST. It may be worthwhile to offer a `--quick` or `--fast` argument, which prefers non-CST parsing even if it means a smaller variety of possible bugs.

## Testing

`py-bugger` currently has a small set of unit and end-to-end tests. The project is still evolving, and there's likely some significant refactoring that will happen before it fully stabilizes internally. We're aiming for test coverage that preserves current functionality, but isn't overly fragile to refactoring. Currently, the focus is on e2e tests for all significant external behavior, and unit tests for critical and stable utilities.

### Unit tests

Unit tests currently require no setup.

### End-to-end tests

End-to-end tests run `py-bugger` commands just as end users would, against a variety of scripts and small projects. This requires a bit of setup that's helpful to understand.

Randomness plays an important role in creating all bugs, so a random seed is set in `tests/e2e_tests/conftest.py`. This is done in `set_random_seed_env()`, which sets an environment variable with session scope.

The `e2e_config()` fixture returns a session-scoped config object containing paths used in most e2e tests. These include reference files, sample scripts, and the path to the Python interpreter for the current virtual environment. Note that this test config object is *not* the same as the `pb_config` object that's used in the main project.

Most e2e test functions copy sample code to a temp directory, and then make a `py-bugger` call using either `--target-dir` or `--target-file` aimed at that directory. Usually, they run the target file as well. We then make various assertions about the bugs that were introduced, and the results of running the file or project after running `py-bugger`.