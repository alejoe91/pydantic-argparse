"""Parses Mapping Pydantic Fields to Command-Line Arguments.

The `mapping` module contains the `should_parse` function, which checks whether
this module should be used to parse the field, as well as the `parse_field`
function, which parses mapping `pydantic` model fields to `ArgumentParser`
command-line arguments.
"""


# Standard
import argparse
import ast
import collections.abc

# Third-Party
import pydantic

# Typing
from typing import Optional

# Local
from pydantic_argparse import utils


def should_parse(field: pydantic.Field) -> bool:
    """Checks whether the field should be parsed as a `mapping`.

    Args:
        field (pydantic.Field): Field to check.

    Returns:
        bool: Whether the field should be parsed as a `mapping`.
    """
    # Check and Return
    return utils.types.is_field_a(field, collections.abc.Mapping)


def parse_field(
    parser: argparse.ArgumentParser,
    field: pydantic.Field,
    name: str = None,
) -> Optional[utils.pydantic.PydanticValidator]:
    """Adds mapping pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.Field): Field to be added to parser.

    Returns:
        Optional[utils.pydantic.PydanticValidator]: Possible validator method.
    """
    # Add Mapping Field
    name, validator_name = utils.arguments.name(field, name=name)
    parser.add_argument(
        name,
        action=argparse._StoreAction,
        help=utils.arguments.description(field),
        dest=field.alias,
        metavar=field.alias.upper(),
        required=bool(field.is_required()),
    )

    # Construct and Return Validator
    return utils.pydantic.as_validator(validator_name, lambda v: ast.literal_eval(v))
