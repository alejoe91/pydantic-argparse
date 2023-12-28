"""Parses Standard Pydantic Fields to Command-Line Arguments.

The `standard` module contains the `parse_field` function, which parses
standard `pydantic` model fields to `ArgumentParser` command-line arguments.

Unlike the other `parser` modules, the `standard` module does not contain a
`should_parse` function. This is because it is the fallback case, where fields
that do not match any other types and require no special handling are parsed.
"""


# Standard
import argparse

# Third-Party
import pydantic

# Typing
from typing import Optional

# Local
from pydantic_argparse import utils


def parse_field(
    parser: argparse.ArgumentParser,
    field: pydantic.Field,
    name: str = None,
) -> Optional[utils.pydantic.PydanticValidator]:
    """Adds standard pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.Field): Field to be added to parser.

    Returns:
        Optional[utils.pydantic.PydanticValidator]: Possible validator method.
    """
    # Add Standard Field
    name, validator_name = utils.arguments.name(field, name=name)
    alias = field.alias if field.alias is not None else name
    parser.add_argument(
        name,
        action=argparse._StoreAction,
        help=utils.arguments.description(field),
        dest=alias,
        metavar=alias.upper(),
        required=bool(field.is_required()),
    )

    # Construct and Return Validator
    return utils.pydantic.as_validator(validator_name, lambda v: v)
