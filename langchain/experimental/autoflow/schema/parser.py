from __future__ import annotations

import json

from langchain.formatting import formatter
from langchain.schema import BaseOutputParser, OutputParserException
from langchain.experimental.autoflow.schema import BaseSchema, SchemaParseError, SchemaType

SCHEMA_FORMAT = """\
You should respond in JSON format:

```json
{schema_format}
```

Do not wrap ```json ``` around the json output, you should only output the json object itself. Ensure the response can be parsed by Python `json.loads`.
"""

class FlowSchemaOutputParser(BaseOutputParser):
    flow_schema: BaseSchema

    def parse(self, text) -> SchemaType:
        text = text.replace("'", '"')
        text = text.replace("True", "true")
        text = text.replace("False", "false")
        text = text.replace("\t", "")

        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as e:
            raise OutputParserException(f"Got invalid JSON object. Error: {e}")

        try:
            schema_obj = self.flow_schema.parse(parsed)
        except SchemaParseError as e:
            raise OutputParserException(f"Got invalid typed output. {e}")
        return schema_obj

    def get_format_instructions(self):
        return formatter.format(SCHEMA_FORMAT, schema_format=self.flow_schema.format())

    @property
    def _type(self):
        return "flow_schema"

# from intellison import safe_parse, llm_parse, safe_parse_with_schema, llm_parse_with_schema