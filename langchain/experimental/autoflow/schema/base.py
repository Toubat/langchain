from __future__ import annotations

from typing import List, Optional, Dict, Any, Union, Type

from pydantic import BaseModel, Extra, root_validator
from abc import ABC, abstractmethod


PrimitiveSchemaType = Union[str, int, float, bool]
ListSchemaType = List[PrimitiveSchemaType]
SchemaType = Union[
    PrimitiveSchemaType,
    ListSchemaType,
    Dict[str, Union[PrimitiveSchemaType, ListSchemaType]],
]


class SchemaParseError(Exception):
    """Error raised when schema parsing fails."""

    def __init__(self, message: str):
        """Initialize a SchemaParseError."""
        super().__init__(message)


def format_primitive_error_message(type_name: str, input: Any) -> str:
    """Format an error message for a primitive type."""
    return f"Expected {type_name}, got {type(input)} for {input}"


class BaseSchema(BaseModel, ABC):
    """Base schema definition."""
    description: Optional[str] = None

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def type_name(self) -> str:
        """Return the type name of this schema."""
        return NotImplementedError

    @abstractmethod
    def parse(self, input: Any) -> Any:
        """Parse input to this schema."""

    def format(self) -> str:
        """Return string representation of this schema."""
        return str(self)

    def __str__(self) -> str:
        """Return string representation of this schema."""
        return f"{self.type_name} ({self.description})" if self.description else self.type_name


class PrimitiveSchema(BaseSchema):
    """Schema for a primitive type."""

    def parse(self, input: Any) -> Any:
        """Parse input to this schema."""
        return NotImplementedError


class StringSchema(PrimitiveSchema):
    """Schema for a string."""

    @property
    def type_name(self) -> str:
        """Return the type name of string schema."""
        return "string"

    def parse(self, input: Any) -> str:
        """Parse input to this schema."""
        if not isinstance(input, str):
            raise SchemaParseError(format_primitive_error_message(self.type_name, input))
        return input


class BooleanSchema(PrimitiveSchema):
    """Schema for a boolean."""

    @property
    def type_name(self) -> str:
        """Return the type name of boolean schema."""
        return "boolean"

    def parse(self, input: Any) -> bool:
        """Parse input to this schema."""
        if not isinstance(input, bool):
            raise SchemaParseError(format_primitive_error_message(self.type_name, input))
        return input


class NumberSchema(PrimitiveSchema):
    """Schema for a number."""

    @property
    def type_name(self) -> str:
        """Return the type name of number schema."""
        return "number"

    def parse(self, input: Any) -> Union[int, float]:
        """Parse input to this schema."""
        if not isinstance(input, (int, float)):
            raise SchemaParseError(format_primitive_error_message(self.type_name, input))
        return input


class ArraySchema(BaseSchema):
    """Schema for an array."""

    description: Optional[str] = f"List of elements of the given type."
    element_type: Union[Type[PrimitiveSchema], PrimitiveSchema]

    @property
    def element_instance(self) -> PrimitiveSchema:
        """Return the instance of element type."""
        if isinstance(self.element_type, type):
            return self.element_type()
        return self.element_type

    @property
    def type_name(self) -> str:
        """Return the type name of array schema."""
        return f"{self.element_instance.type_name}[]"

    def parse(self, input: Any) -> List[Any]:
        """Parse input to this schema."""
        if not isinstance(input, list):
            raise SchemaParseError(format_primitive_error_message(self.type_name, input))
        return [self.element_instance.parse(item) for item in input]


class ObjectSchema(BaseSchema):
    """Schema for an object."""

    fields: Dict[str, Union[PrimitiveSchema, ArraySchema]]

    @property
    def type_name(self) -> str:
        """Return the type name of object schema."""
        attr_str = "\n".join(
            [f"  \"{key}\": {field.type_name}, ({field.description})" if field.description else f"  \"{key}\": {field.type_name}," for key, field in self.fields.items()]
        )
        return "\n".join(["{", attr_str, "}"])

    def parse(self, input: Any) -> dict:
        """Parse input to this schema."""
        if not isinstance(input, dict):
            raise SchemaParseError(format_primitive_error_message(self.type_name, input))

        # check if all required keys are present
        for key, field in self.fields.items():
            if key not in input:
                raise SchemaParseError(f"Expected key \"{key}\" of type {field.type_name} in {input}")

        # check if extra keys are present
        for key in input.keys():
            if key not in self.fields:
                raise SchemaParseError(f"Unexpected key \"{key}\" in {input}, the expected keys are {self.fields.keys()}")

        # parse each field
        return {key: field.parse(input[key]) for key, field in self.fields.items()}

    def __str__(self) -> str:
        """Return string representation of this schema."""
        return self.type_name