"""A set of tasks to be used for common jobs."""

from io import StringIO
import json
from pathlib import Path
import re
import sys
import webbrowser

import anybadge
from invoke import Context, task
from pretty_html_table import build_table
import tablib

SRC_ROOT_DIR = Path(__file__).resolve().parent / "ricardo" / "ee"
SRC_STEM_DIR = "fastapi"
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


@task(aliases=["vuln-scan"])
def vulnerability_scan(
    ctx: Context, badge_path: str | None = None, log_path: str | None = None
) -> None:
    """Scan for potential security vulnerabilities in included packages."""
    print("***** Running pip-audit *****")

    output = StringIO()
    result = ctx.run("pip-audit --skip-editable", out_stream=output, warn=True)

    print(result.stdout)

    vulnerabilities_str = result.stderr.splitlines()[0]
    expected_pattern = r"Found (\d+) known vulnerabilit(?:y|ies) in \d+ packages?"

    if vulnerabilities_str == "No known vulnerabilities found":
        vulnerabilities = "0"
    elif str_match := re.match(expected_pattern, result.stderr):
        vulnerabilities = str_match[1]
    else:
        raise ValueError(f"Unexpected output from pip-audit: {result.stderr}")

    if badge_path is not None:
        badge = anybadge.Badge(
            "vulnerabilities", vulnerabilities, thresholds={1: "green", 2: "red"}
        )
        badge.write_badge(badge_path)

    if log_path is not None:
        Path(log_path).write_text(f"{result.stderr}\n{result.stdout}")


@task
def show_coverage_report(ctx: Context) -> None:
    """Generate HTML coverage report and open in browser."""
    ctx.run("coverage html")
    webbrowser.open_new_tab(str(Path("./coverage_report/index.html").resolve()))


@task(
    help={
        "part": "Part of semantic version to increment",
        "dry-run": "Show changes that would be made, but don't change, commit or tag",
    }
)
def bump(ctx: Context, part: str, dry_run: bool = False) -> None:
    """Bump the package version according to the semantic version part, git tag it."""
    current_branch = ctx.run(
        "git rev-parse --abbrev-ref HEAD", hide="out"
    ).stdout.splitlines()[0]

    if current_branch != "main":
        sys.exit("Must be on branch `main` to bump version")

    if dry_run:
        ctx.run(f"bump2version --verbose --dry-run {part}")
    else:
        ctx.run(f"bump2version {part}")
        print("You should now run:\n    git push --follow-tags")


@task
def license_check(
    ctx: Context, badge_path: str | None = None, log_path: str | None = None
) -> None:
    """Check the license of all dependencies."""
    whitelist = [
        "MIT License",
        "MIT",
        "BSD License",
        "Python Software Foundation License",
        "Apache Software License",
        "Academic Free License",
        "The Unlicense (Unlicense)",
    ]

    result = ctx.run(
        "pip-licenses --format=json --with-description --with-urls",
    )
    json_string = StringIO(result.stdout)

    package_licenses = json.load(json_string)

    # Filter out packages with licenses not in whitelist
    bad_licenses = [
        package
        for package in package_licenses
        if (
            any(
                single_license not in whitelist
                for single_license in package["License"].split("; ")
            )
        )
    ]

    # Sort licenses on "License" key
    bad_licenses = sorted(bad_licenses, key=lambda k: k["License"])

    print(bad_licenses)

    if badge_path is not None:
        badge = anybadge.Badge(
            "license flags", len(bad_licenses), thresholds={1: "green", 2: "red"}
        )
        badge.write_badge(badge_path)

    if log_path is not None:
        # Load bad licenses into tablib
        data = tablib.Dataset()
        data.headers = ["Name", "Version", "License", "URL", "Description"]
        for package in bad_licenses:
            if package["URL"] == "UNKNOWN":
                url = "UNKNOWN"
            else:
                url = f'<a target="_blank" href="{package["URL"]}">{package["URL"]}</a>'

            data.append(
                [
                    package["Name"],
                    package["Version"],
                    package["License"],
                    url,
                    package["Description"],
                ]
            )
        raw_html = data.export("df")

        html_table = build_table(raw_html, "blue_light", escape=False)

        # Write tablib to file
        with Path(log_path).open("w") as f:
            f.write(html_table)


@task
def create_jupyter_kernel(ctx: Context) -> None:
    """Create a jupyter kernel from the virtual environment."""
    ctx.run("poetry run python -m ipykernel install --user --name=fastapi")
