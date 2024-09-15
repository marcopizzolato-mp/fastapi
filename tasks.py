"""A set of tasks to be used for common jobs."""

from pathlib import Path

from invoke import Context, task

SRC_ROOT_DIR = Path(__file__).resolve().parent / "ricardo" / "ee"
SRC_STEM_DIR = "fastapi_application"
SRC_DIR = SRC_ROOT_DIR / SRC_STEM_DIR


@task
def lint(ctx: Context, check: bool = False, junitxml: str | None = None) -> None:
    """Run linting over code with the check param if specified."""
    print("***** Running ruff check *****")
    # Can't get junit output and print to screen from ruff in one shot, so run it twice
    check_str_ruff = "--no-fix" if check else ""
    if junitxml:
        ctx.run(
            f"ruff check . {check_str_ruff} --output-format junit --exit-zero "
            f">> {junitxml}"
        )
    ctx.run(f"ruff check . {check_str_ruff}")

    print("***** Running ruff format *****")
    format_check = "--check" if check else ""
    ctx.run(f"ruff format . {format_check}")

    print("***** Running mdformat *****")
    check_str_mdformat = "--check" if check else ""
    ctx.run(f"mdformat . {check_str_mdformat}")


@task
def test(ctx: Context, junitxml: str | None = None) -> None:
    """Run unit tests."""
    print("***** Running pytest *****")

    junit_str = f" --junitxml={junitxml}" if junitxml else ""
    ctx.run(
        f'pytest "{SRC_DIR}" '
        "--cov=ricardo "
        "--cov-report html "
        "--suppress-no-test-exit-code "
        f"{junit_str} ",
    )


@task
def type_check(ctx: Context, junitxml: str | None = None) -> None:
    """Run type checking."""
    print("***** Running mypy *****")

    junit_str = f" --junit-xml={junitxml}" if junitxml else ""
    ctx.run(f'mypy "{SRC_DIR}" {junit_str}')


@task
def create_jupyter_kernel(ctx: Context) -> None:
    """Create a jupyter kernel from the virtual environment."""
    ctx.run("poetry run python -m ipykernel install --user --name=fastapi_application")
