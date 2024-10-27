from __future__ import annotations

import os

import nox


ROOT = os.path.dirname(os.path.abspath(__file__))


@nox.session
def build(session: nox.Session) -> None:
    """Build sdist and wheel dists."""
    session.install("pip", "build")
    session.install("setuptools")
    session.run("python", "--version")
    session.run("pip", "--version")
    session.run("python", "-m", "build")


@nox.session
def install(session: nox.Session) -> None:
    first_arg = session.posargs[0] if session.posargs else None

    if first_arg:
        if os.path.isfile(first_arg):
            session.install(first_arg)
        elif os.path.isdir(first_arg):
            session.install(
                "sensible_bmi", f"--find-links={first_arg}", "--no-deps", "--no-index"
            )
        else:
            session.error("path must be a source distribution or folder")
    else:
        session.install(".")


@nox.session
def test(session: nox.Session) -> None:
    """Run the tests."""
    session.install("-r", "requirements-testing.in", "-r", "requirements.in")
    install(session)

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
