from __future__ import annotations

from typing import Dict, Union
from pydantic import BaseModel, Extra

from langchain.experimental.autoflow.schema.base import (
    SchemaParseError,
    NumberSchema,
    StringSchema,
    BooleanSchema,
    ArraySchema,
    ObjectSchema,
    PrimitiveSchema,
    BaseSchema,
    PrimitiveSchemaType,
    ListSchemaType,
    SchemaType,
)
from langchain.experimental.autoflow.schema.parser import FlowSchemaOutputParser

class Schema(BaseModel):
    """Class containing method for instantiating schema objects."""

    class Config:
        """Configuration for Schema object."""
        extra = Extra.forbid

    @staticmethod
    def number(description: str = None) -> NumberSchema:
        """Create a number schema."""
        return NumberSchema(description=description)

    @staticmethod
    def string(description: str = None) -> StringSchema:
        """Create a string schema."""
        return StringSchema(description=description)

    @staticmethod
    def boolean(description: str = None) -> BooleanSchema:
        """Create a boolean schema."""
        return BooleanSchema(description=description)

    @staticmethod
    def array(schema: PrimitiveSchema, description: str = None) -> ArraySchema:
        """Create an array schema."""
        return ArraySchema(element_type=schema, description=description)

    @staticmethod
    def object(**kwargs) -> ObjectSchema:
        """Create an object schema."""
        return ObjectSchema(fields={**kwargs})

__all__ = [
    "Schema",
    "SchemaParseError",
    "NumberSchema",
    "StringSchema",
    "BooleanSchema",
    "ArraySchema",
    "ObjectSchema",
    "BaseSchema",
    "PrimitiveSchema",
    "PrimitiveSchemaType",
    "ListSchemaType",
    "SchemaType",
    "FlowSchemaOutputParser"
]
