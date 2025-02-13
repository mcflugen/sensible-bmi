from __future__ import annotations

import os

import nox


ROOT = os.path.dirname(os.path.abspath(__file__))


@nox.session
def test(session: nox.Session) -> None:
    """Run the tests."""
    session.install(".[testing]")

    session.run("coverage", "run", "--branch", "--module", "pytest")
    session.run("coverage", "report", "--ignore-errors", "--show-missing")
    session.run("coverage", "xml", "-o", "coverage.xml")

@nox.session
def lint(session: nox.Session) -> None:
    """Look for lint."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")
