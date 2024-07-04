# Developer Documentation

## Set up development environment

This project uses `poetry`, which we recommend installing
[with `pipx`](https://python-poetry.org/docs/#installing-with-pipx). For more
information on development tools setup see the
[Python development tools](https://data-science.rcdo.co.uk/core/operations-manual/onboarding/standard_software_setup/#python-development-tools)
section of the Data Science Team Operations Manual.

To build the Python development environment, navigate to the base directory of this
project and run:

```commandline
poetry install
```

If you have JupyterLab installed at system level (e.g. with `pipx`), and do not need the
notebook dependencies with the project, install with:

```commandline
poetry install --without notebook --sync
```

Create the named kernel for Jupyter from the virtual environment:

```commandline
poetry run invoke create-jupyter-kernel
```

Install the pre-commit hooks:

```commandline
poetry run pre-commit install
```

## Updating project boilerplate

This project was created from a
[cookiecutter](https://github.com/cookiecutter/cookiecutter) template using
[`project-setup-tool`](https://gitlab.rcdo.co.uk/data-science/core/project-setup-tool).

To benefit from bug fixes and enhancements `project-setup-tool` should be installed
with:

```commandline
pipx install ricardo-ee-project-setup-tool
```

and this project should be regularly updated with:

```commandline
project-setup-tool update
```

See the `project-setup-tool`
[README](https://gitlab.rcdo.co.uk/data-science/core/project-setup-tool/-/blob/main/README.md)
for more details.

## Project data

The `data/` directory is included in `.gitignore` so data stored there will not be
committed to the repository. DVC should be used if data needs to be included in version
control. See the Data Science Operations Manual best practice section on
[Data](https://data-science.rcdo.co.uk/core/operations-manual/best_practice/data) for
more information.

## Jupyter Notebook Support

This project uses Jupyter notebooks, which can be started from the poetry environment
with:

```commandline
poetry run jupyter lab
```

### Notebook version control

[Jupytext](https://github.com/mwouts/jupytext) is installed with the development
dependencies in this project to assist with Jupyter notebook version control. The
project is configured such that Jupytext will automatically save a 'paired notebook' of
any `.ipynb` file as python percent format copies (`.py` files with notebook cells
delineated by `#%%` comments) whenever a `.ipynb` file is modified. Only the `.py` file
is committed to the repository, which can be used to re-build the `.ipynb` file locally
just by opening it in JupyterLab.

For guidance and good practice when using Jupyter notebooks see the Data Science
Operations Manual section on
[Notebooks](https://data-science.rcdo.co.uk/core/operations-manual/best_practice/notebooks/#notebooks).

## Developer task automation

Common development tasks are automated using [`invoke`](https://www.pyinvoke.org).

To see a list of available tasks run:

```
invoke --list
```

## Development workflow

The basic developer workflow is as follows:

1. Create a branch
1. Make a code change
1. `poetry run invoke lint` to run autoformatting and code analysis checks.
1. `poetry run invoke type-check` to test the typing of variables
1. `poetry run invoke test` to run all the tests
1. Commit the change
1. Repeat from step 2 as required
1. Push the new branch to GitLab
1. Create a merge request in GitLab
1. Assign for code review.

For more information, see the Data Science Operations Manual section on
[Development](https://data-science.rcdo.co.uk/core/operations-manual/project_lifecycle/development/#development).

## Unit tests

The [`pytest`](https://docs.pytest.org/en/latest/) framework is used for unit tests and
[`coverage`](https://coverage.readthedocs.io/) is used to report on sections of code
that are untested. Tests and the coverage report can be run using the invoke tasks with:

```commandline
poetry run invoke test
```

and

```commandline
poetry run invoke show-coverage-report
```

For more information on writing tests and using test coverage, see the Data Science
Operations Manual section on
[Testing code](https://data-science.rcdo.co.uk/core/operations-manual/best_practice/python/#testing-code).

## Making releases off the `main` branch

The GitLab [CI pipeline](https://docs.gitlab.com/ee/ci/) is set up such that
incrementing the version number will trigger a deployment of the latest version of the
app in our internal company repository.

The following steps will increment the version number in the python package and the git
tag simultaneously and deploy the package:

1. Ensure `main` is up-to-date locally.
1. Bump the [semantic version](https://semver.org/) tag with one of the following:
   - `poetry run invoke bump major` for major API breaking changes
   - `poetry run invoke bump minor` for new backwards-compatible functionality
   - `poetry run invoke bump patch` for backwards-compatible bug fixes
1. Push the new commit and the tag to GitLab with `git push --follow-tags`
