from __future__ import annotations

import os

import nox


ROOT = os.path.dirname(os.path.abspath(__file__))


@nox.session
def test(session: nox.Session) -> None:
    """Run the tests."""
    session.install(".[testing]")

    args = ["--cov", "sensible_bmi", "-vvv"] + session.posargs

    if "CI" in os.environ:
        args.append(f"--cov-report=xml:{ROOT}/coverage.xml")
    session.run("pytest", *args)

    if "CI" not in os.environ:
        session.run("coverage", "report", "--ignore-errors", "--show-missing")


@nox.session
def lint(session: nox.Session) -> None:
    """Look for lint."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")
