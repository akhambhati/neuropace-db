# tests/test_version.py

import neuropace_db


def test_has_version():
    assert neuropace_db.__version__ is not None
