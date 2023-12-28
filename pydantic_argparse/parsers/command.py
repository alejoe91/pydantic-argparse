"""Parses Nested Pydantic Model Fields to Sub-Commands.

The `command` module contains the `should_parse` function, which checks whether
this module should be used to parse the field, as well as the `parse_field`
function, which parses nested `pydantic` model fields to `ArgumentParser`
sub-commands.
"""


# Standard
import argparse

# Third-Party
import pydantic

# Typing
from typing import Optional

# Local
from pydantic_argparse import utils


def should_parse(field: pydantic.Field) -> bool:
    """Checks whether the field should be parsed as a `command`.

    Args:
        field (pydantic.Field): Field to check.

    Returns:
        bool: Whether the field should be parsed as a `command`.
    """
    # Check and Return
    return utils.types.is_field_a(field, pydantic.BaseModel)


def parse_field(
    subparser: argparse._SubParsersAction,
    field: pydantic.Field,
    name: str = None,
) -> Optional[utils.pydantic.PydanticValidator]:
    """Adds command pydantic field to argument parser.

    Args:
        subparser (argparse._SubParsersAction): Sub-parser to add to.
        field (pydantic.Field): Field to be added to parser.

    Returns:
        Optional[utils.pydantic.PydanticValidator]: Possible validator method.
    """
    # Add Command
    name = field.alias if field.alias is not None else name
    subparser.add_parser(
        name,
        help=field.description,
        model=field.annotation,  # type: ignore[call-arg]
        exit_on_error=False,  # Allow top level parser to handle exiting
    )

    # Return
    return None
