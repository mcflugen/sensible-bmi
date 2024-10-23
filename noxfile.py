from __future__ import annotations

import os

import nox


ROOT = os.path.dirname(os.path.abspath(__file__))


@nox.session
def test(session: nox.Session) -> None:
    """Run the tests."""
    session.install(".[testing]")

    session.run(
        "coverage",
        "run",
        "--branch",
        "--source=sensible_bmi,tests",
        "--module",
        "pytest",
    )
    session.run("coverage", "report", "--ignore-errors", "--show-missing")
    session.run("coverage", "xml", "-o", "coverage.xml")


@nox.session
def lint(session: nox.Session) -> None:
    """Look for lint."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")


@nox.session(name="docs-build")
def docs_build(session: nox.Session) -> None:
    """Build the docs."""
    session.install(".", "-r", "requirements-docs.in")

    os.makedirs("build", exist_ok=True)
    docs_build_api(session)
    session.run(
        "sphinx-build",
        *("-j", "auto"),
        *("-b", "html"),
        "-W",
        "--keep-going",
        "docs/",
        "build/html",
    )
    session.log("generated docs at build/html")


@nox.session(name="docs-build-api")
def docs_build_api(session: nox.Session) -> None:
    docs_dir = "docs/"
    generated_dir = os.path.join(docs_dir, "generated", "api")

    session.install(".", "-r", "requirements-docs.in")

    session.log(f"generating api docs in {generated_dir}")
    session.run(
        "sphinx-apidoc",
        "-e",
        "-force",
        "--no-toc",
        "--module-first",
        *("-d", "2"),
        # f"--templatedir={docs_dir / '_templates'}",
        *("-o", generated_dir),
        "src/sensible_bmi",
        "*.pyx",
        "*.so",
    )
