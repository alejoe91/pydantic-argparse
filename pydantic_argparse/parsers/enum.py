"""Parses Enum Pydantic Fields to Command-Line Arguments.

The `enum` module contains the `should_parse` function, which checks whether
this module should be used to parse the field, as well as the `parse_field`
function, which parses enum `pydantic` model fields to `ArgumentParser`
command-line arguments.
"""


# Standard
import argparse
import enum

# Third-Party
import pydantic

# Local
from pydantic_argparse import utils

# Typing
from typing import Optional, Type


def should_parse(field: pydantic.Field) -> bool:
    """Checks whether the field should be parsed as an `enum`.

    Args:
        field (pydantic.Field): Field to check.

    Returns:
        bool: Whether the field should be parsed as an `enum`.
    """
    # Check and Return
    return utils.types.is_field_a(field, enum.Enum)


def parse_field(
    parser: argparse.ArgumentParser,
    field: pydantic.Field,
    name: str = None,
) -> Optional[utils.pydantic.PydanticValidator]:
    """Adds enum pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.Field): Field to be added to parser.

    Returns:
        Optional[utils.pydantic.PydanticValidator]: Possible validator method.
    """
    # Extract Enum
    enum_type: Type[enum.Enum] = field.annotation

    # Compute Argument Intrinsics
    is_flag = len(enum_type) == 1 and not bool(field.is_required())
    is_inverted = is_flag and field.get_default() is not None and field.allow_none

    # Determine Argument Properties
    metavar = f"{{{', '.join(e.name for e in enum_type)}}}"
    action = (
        argparse._StoreConstAction if is_flag
        else argparse._StoreAction
    )
    const = (
        {} if not is_flag
        else {"const": None} if is_inverted
        else {"const": list(enum_type)[0]}
    )

    # Add Enum Field
    argument_name, validator_name = utils.arguments.name(field, is_inverted, name=name)
    dest_name = field.alias if field.alias is not None else name

    parser.add_argument(
        argument_name,
        action=action,
        help=utils.arguments.description(field),
        dest=dest_name,
        metavar=metavar,
        required=bool(field.is_required()),
        **const,  # type: ignore[arg-type]
    )

    # Construct and Return Validator
    return utils.pydantic.as_validator(validator_name, lambda v: enum_type[v])
