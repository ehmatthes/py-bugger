py-bugger
===

When people learn debugging, they typically have to learn it by focusing on whatever bugs come up in their code. They don't get to work on specific kinds of errors, and they don't get the chance to progress from simple to more complex bugs. This is quite different from how we teach and learn just about any other skill.

`py-bugger` lets you intentionally introduce specific kinds and numbers of bugs to a working project. You can introduce bugs to a project with a single file, or a much larger project. This is much different from the typical process of waiting for your next bug to show up, or introducing a bug yourself. `py-bugger` gives people a structured way to learn debugging, just as we approach all other areas of programming.

Example usage
---

`py-bugger` acts on directories, so consider a directory with just one file, *name_picker.py*. It chooses a single name from a list of names, and announces the winner:

```sh
$ python name_picker.py
The winner: Willie!
```

To practice debugging, we'll introduce a `ModuleNotFoundError`:

```sh
$ pip install python-bugger
$ py-bugger --exception-type ModuleNotFoundError
Introducing a ModuleNotFoundError...
  Modified file.
```

(The package name `py-bugger` was not available on PyPI. I'll make sure the repo name and the package name are consistent before a 1.0 release.)

Now, run the project again and you should see it fail:

```sh
$ python name_picker.py
Traceback (most recent call last):
  File "name_picker.py", line 1, in <module>
    import rando
ModuleNotFoundError: No module named 'rando'
```

You can open your file, and practice debugging. If you get the project working again, great!

If you get stuck, all the bugs that were introduced are contained in a single Git commit. You can see those bugs using `git diff`.

Current state
---

This project is a proof of concept at the moment; I'm releasing it at this stage to get feedback about whether it's a useful tool. It should work on all OSes, but it only introduces two kinds of bug. If there's any interest at all in this project, I'll quickly bring it to a more usable state.

### Usage:

```sh
Usage: py-bugger [OPTIONS]

  Practice debugging, by intentionally introducing bugs into an existing
  codebase.

Options:
  -e, --exception-type TEXT  What kind of exception to induce.
  --target-dir TEXT          What code directory to target. (Be careful when
                             using this arg!)
  --target-file TEXT         Target a single .py file.
  -n, --num-bugs INTEGER     How many bugs to introduce.
  --help                     Show this message and exit.
```

### Trying `py-bugger`

If you're interested in trying the project at this early stage, do the following:

- Make a new directory with a single .py file in it.
- Make sure the .py file has at least one `import` statement if you're targing `ModuleNotFoundError`. If you're targeting `AttributeError`, make sure the file has at least one attribute.
- Run your file, and make sure it works.
- Make an initial Git commit.
- Install `python-bugger`.
- Run `py-bugger -e ModuleNotFoundError`, or `py-bugger -e AttributeError`.
- Run your project, and see if it generates the requested exception.

You can also clone a working Python project from GitHub, and then install and run `py-bugger`. If you run the project, you should see the expected error. If you run the test suite, it should fail in the expected way.

Brief Roadmap
---

If this project is useful or interesting to people, here's a brief roadmap of where I'm planning to take it:

- Check for a clean Git state before introducing any bugs.
- Make a new commit after introducing bugs.
- Clarify usage docs, so people only introduce bugs where they want them to be.
- Expand the variety of exception types that can be introduced.
- Expand the variety of possible causes for inducing specific exceptions.
- Visit all files not in .gitignore, and not in a tests/ dir.
- Generate logical (non-crashing) errors as well as specific exception types.
- Expand usage to allow an arbitrary number and kind of bugs.
- Develop a list of good projects to practice against. ie, clone <project> from GitHub, run its tests, run `py-bugger`, and practice debugging.

Contributing
---

If you're interested in this project, please feel free to get in touch. If you have general feedback or just want to see the project progress, please share your thoughts in the [Initial feedback](https://github.com/ehmatthes/py-bugger/discussions/7) discussion. Also, feel free to [open a new issue](https://github.com/ehmatthes/py-bugger/issues/new).
