"""Parses Boolean Pydantic Fields to Command-Line Arguments.

The `boolean` module contains the `should_parse` function, which checks whether
this module should be used to parse the field, as well as the `parse_field`
function, which parses boolean `pydantic` model fields to `ArgumentParser`
command-line arguments.
"""


# Standard
import argparse

# Third-Party
import pydantic

# Typing
from typing import Optional

# Local
from pydantic_argparse import utils
from pydantic_argparse.argparse import actions


def should_parse(field: pydantic.Field) -> bool:
    """Checks whether the field should be parsed as a `boolean`.

    Args:
        field (pydantic.Field): Field to check.

    Returns:
        bool: Whether the field should be parsed as a `boolean`.
    """
    # Check and Return
    return utils.types.is_field_a(field, bool)


def parse_field(
    parser: argparse.ArgumentParser,
    field: pydantic.Field,
    name: str = None,
) -> Optional[utils.pydantic.PydanticValidator]:
    """Adds boolean pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.Field): Field to be added to parser.

    Returns:
        Optional[utils.pydantic.PydanticValidator]: Possible validator method.
    """
    # Compute Argument Intrinsics
    is_inverted = not field.is_required() and bool(field.get_default())

    # Determine Argument Properties
    action = (
        actions.BooleanOptionalAction if field.is_required()
        else argparse._StoreFalseAction if is_inverted
        else argparse._StoreTrueAction
    )

    # Add Boolean Field
    name, validator_name = utils.arguments.name(field, is_inverted, name)

    parser.add_argument(
        name,
        action=action,
        help=utils.arguments.description(field),
        dest=field.alias,
        required=bool(field.is_required()),
    )

    # Construct and Return Validator
    return utils.pydantic.as_validator(validator_name, lambda v: v)
