# Suggestions of projects for py-bugger practice
This list includes open-source projects that could be ideal for practicing debugging with tools like `py-bugger`. 

Observations:
- I didn't run their test suites, but, based on my experience using some of these libraries/packages, I would expect failure times to be **~2-3 minutes or less** (not necessarily running the whole test suite though).
- These projects are particularly appealing for debugging practice because they offer **clear visual feedback** through terminal outputs and rendered UIs or **immediate syntax/runtime failures** when bugs are introduced.

Projects listed here:
- Are actively maintained
- Provide fast failure feedback on tests
- Offer relevant opportunities to practice inducing and diagnosing bugs

| Project | Description | Reason |
|--------|-------------|---------------|
| [rich](https://github.com/Textualize/rich) | Terminal formatting | Visual feedback and modular code |
| [httpx](https://github.com/encode/httpx) | Async HTTP client | Great for I/O bugs and async tracing |
| [black](https://github.com/psf/black) | Code formatter | Deterministic behavior, regression testing |
| [py-shinywidgets](https://github.com/posit-dev/py-shinywidgets) | Widgets for Shiny apps | Component-level testing and user interaction logic |
| [pydantic](https://github.com/pydantic/pydantic) | Type-based validation | Complex logic with excellent coverage |
| [typer](https://github.com/tiangolo/typer) | CLI builder | Good for simulating user input/output |
| [Shiny for Python](https://github.com/posit-dev/py-shiny) | Web framework for interactive data apps | Modular code, fast tests, good UI/server bug surface |
| [python-dateutil](https://github.com/dateutil/dateutil) | Date/time parsing | Handles real-world edge cases |