"""Namespaces Utility Functions for Declarative Typed Argument Parsing.

The `namespaces` module contains a utility function used for recursively
converting `argparse.Namespace`s to regular Python `dict`s.
"""


# Standard
import argparse

# Typing
from typing import Any, Dict


def to_dict(namespace: argparse.Namespace) -> Dict[str, Any]:
    """Converts a nested namespace to a dictionary recursively.

    Args:
        namespace (argparse.Namespace): Namespace object to convert.

    Returns:
        Dict[str, Any]: Nested dictionary generated from namespace.
    """
    # Get Dictionary from Namespace Vars
    dictionary = vars(namespace)

    # Loop Through Dictionary
    for (key, value) in dictionary.items():
        # Check for Namespace Objects
        if isinstance(value, argparse.Namespace):
            # Recurse
            dictionary[key] = to_dict(value)

    # split nested structure
    keys = list(dictionary.keys())
    for key in keys:
        if "/" in key:
            sub_keys = key.split("/")
            value = dictionary.pop(key)
            parent_dict = dictionary
            for sub_key in sub_keys[:-1]:
                # recureively add sub-dictionaries
                if sub_key not in parent_dict:
                    parent_dict[sub_key] = {}
                parent_dict = parent_dict[sub_key]
            parent_dict[sub_keys[-1]] = value

    # Return
    return dictionary
