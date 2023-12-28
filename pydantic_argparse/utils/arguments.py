"""Arguments Utility Functions for Declarative Typed Argument Parsing.

The `arguments` module contains utility functions used for formatting argument
names and formatting argument descriptions.
"""


# Third-Party
import pydantic


def name(field: pydantic.Field, invert: bool = False, name: str = None) -> str:
    """Standardises argument name.

    Args:
        field (pydantic.Field): Field to construct name for.
        invert (bool): Whether to invert the name by prepending `--no-`.

    Returns:
        str: Standardised name of the argument.
        str: Validator name odf the argument.
    """
    # Construct Prefix
    prefix = "--no-" if invert else "--"

    if field.alias is None:
        assert name is not None, "Argument name must be specified if field has no alias."
        argument_name = f"{prefix}{name.replace('_', '-')}"
    else:
        argument_name = f"{prefix}{field.alias.replace('_', '-')}"
        if name is None:
            name = field.alias
    validator_name = name        

    validator_name = name
    print(f"Arg name: {argument_name} -- Validator name: {validator_name}")

    # Prepend prefix, replace '_' with '-'
    return argument_name, validator_name


def description(field: pydantic.Field) -> str:
    """Standardises argument description.

    Args:
        field (pydantic.Field): Field to construct description for.

    Returns:
        str: Standardised description of the argument.
    """
    # Construct Default String
    default = f"(default: {field.get_default()})" if not field.is_required() else None

    # Return Standardised Description String
    return " ".join(filter(None, [field.description, default]))
