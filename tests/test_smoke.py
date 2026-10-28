"""Skeleton smoke test so CI is green on the initial repository setup."""
import app


def test_package_importable():
    assert app.__doc__
