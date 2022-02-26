# noxfile.py
import nox

locations = "src", "tests", "noxfile.py"

@nox.session(python=["3.8", "3.9", "3.10"])
def tests(session):
    session.run("poetry", "install", external=True)
    session.run("pytest", "--cov")

@nox.session(python=["3.8", "3.9", "3.10"])
def lint(session):
    args = session.posargs or locations
    session.install("flake8")
    session.run("flake8", *args)
