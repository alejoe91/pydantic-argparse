"""Declarative and Typed Argument Parsing.

This package contains the classes and methods required for declarative and
typed argument parsing.

The public interface exposed by this package is the `ArgumentParser` class,
which is intended to be a *near* drop-in replacement for the Python standard
library `argparse.ArgumentParser` - while providing declarative and typed
argument parsing.
"""

# Local
import pydantic_argparse.argparse.patches
from .actions import BooleanOptionalAction
from .parser import ArgumentParser

# Public Re-Exports
__all__ = (
    "ArgumentParser",
    "BooleanOptionalAction"
)
