
![py-bugger logo](https://raw.githubusercontent.com/ehmatthes/py-bugger/main/assets/logo_raw_bordered.png)

py-bugger
===

When people learn debugging, they typically have to learn it by focusing on whatever bugs come up in their code. They don't get to work on specific kinds of errors, and they don't get the chance to progress from simple to more complex bugs. This is quite different from how we teach and learn just about any other skill.

`py-bugger` lets you intentionally introduce specific kinds and numbers of bugs to a working project. You can introduce bugs to a project with a single file, or a much larger project. This is much different from the typical process of waiting for your next bug to show up, or introducing a bug yourself. `py-bugger` gives people a structured way to learn debugging, just as we approach all other areas of programming.

Full documentation is at [https://py-bugger.readthedocs.io/](https://py-bugger.readthedocs.io/en/latest/).

Installation
---

```sh
$ pip install python-bugger
```

Note: The package name is python-bugger, because py-bugger was unavailable on PyPI.

## Basic usage

If you don't specify a target directory or file, `py-bugger` will look at all *.py* files in the current directory before deciding where to insert a bug. If the directory is a Git repository, it will follow the rules in *.gitignore*. It will also avoid introducing bugs into test directories and virtual environments that follow familiar naming patterns.

`py-bugger` creates bugs that induce specific exceptions. Here's how to create a bug that generates a `ModuleNotFoundError`:

```sh
$ py-bugger -e ModuleNotFoundError
Introducing a ModuleNotFoundError...
  Modified file.
```

When you run the project again, it should fail with a `ModuleNotFoundError`.

For more details, see the [Quick Start](https://py-bugger.readthedocs.io/en/latest/quick_start/) and [Usage](https://py-bugger.readthedocs.io/en/latest/usage/) pages in the official [docs](https://py-bugger.readthedocs.io/en/latest/).


Contributing
---

If you're interested in this project, please feel free to get in touch. If you have general feedback or just want to see the project progress, please share your thoughts in the [Initial feedback](https://github.com/ehmatthes/py-bugger/discussions/7) discussion. Also, feel free to [open a new issue](https://github.com/ehmatthes/py-bugger/issues/new). The [contributing](https://py-bugger.readthedocs.io/en/latest/contributing/) section in the official docs has more information about how to contribute.
