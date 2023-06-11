from __future__ import annotations

import json
import re

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


def extract_char_idx(error_message):
    print(error_message)
    match = re.search(r'\(char (\d+)\)', error_message)
    if match:
        return int(match.group(1))
    else:
        return None


class FlowSchemaOutputParser(BaseOutputParser):
    flow_schema: BaseSchema

    def parse(self, text) -> SchemaType:
        text = text.replace("'", '"')
        text = text.replace("True", "true")
        text = text.replace("False", "false")
        text = text.replace("\t", "")
        text = text.replace("\\t", "")
        text = text.replace("\n", "")
        text = text.replace("\\n", "")

        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as e:
            if e.msg.startswith("Expecting ',' delimiter"):
                l_idx = e.pos - 1
                r_idx = l_idx + 1

                while text[r_idx] != '"':
                    r_idx += 1

                return self.parse(text[:l_idx] + '\\"' +
                                  text[l_idx+1:r_idx] + '\\"' + text[r_idx+1:])

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
