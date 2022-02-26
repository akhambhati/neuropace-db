# noxfile.py
import tempfile
import nox
nox.options.sessions = "lint", "safety", "tests"

locations = "src", "tests", "noxfile.py"


def install_with_constraints(session, *args, **kwargs):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=["3.8", "3.9", "3.10"])
def tests(session):
    session.run("poetry", "install", external=True)
    session.run("pytest", "--cov")


@nox.session(python=["3.8", "3.9", "3.10"])
def lint(session):
    args = session.posargs or locations
    install_with_constraints(session, "flake8", "flake8-bandit", "flake8-black", "flake8-bugbear", "flake8-import-order")
    session.run("flake8", *args)


@nox.session(python="3.10")
def black(session):
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python="3.8")
def safety(session):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(safety, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")
