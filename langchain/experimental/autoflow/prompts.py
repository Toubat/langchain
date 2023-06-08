
"""

System Prefix
Tools List

Task Description

Previous Attempts:
...

Format Instructions

->

Breakdown Subtasks Description in Natural Language

->

if need refine subtasks:
    goto first step

->

for each subtask description:
    if subtask is solvable using a tool:
        output tool name and input schema
    else:
        output subtask description and input/output schema
        recurse on subtask description
"""


TASK_BREAKDOWN = """\
You are acted as a task breakdown expert. Your job is to breakdown a task into a list of subtasks that potentially can be solved by existing tools.
Subtasks form a dependency flow graph that solve the main task, so that one subtask may depends on the output of other subtasks.

[TOOL_DESCRIPTION]
You have access to a set of tools with their description:
{% for tool in tools %}
- {{ tool.name }}: {{ tool.description }}
{% endfor %}

[TASK_DESCRIPTION]
The task you are working on is:
{{ task }}

[INPUT_CONTEXT]
Here is the input context given to you (necessary for solving the main task):
{{ input_schema }}

[OUTPUT_SCHEMA]
Here is the output schema of the task:
{{ output_schema }}

[PREVIOUS_ATTEMPTS]
Here are the previous attempts of breaking down the task and the critiques of each attempt:
{% for attempt in attempt_history %}
{{ attempt }}
{% endfor %}

Based on existing tools, task description, input context, and output schema, you should to the following steps:
1. Think about whether the main task can be solved by existing tools.
2. If main task is solvable, breakdown the main task into a list of subtasks in natural language.
3. Evaluate the subtask list, reflect on how to improve the current subtask list if possible.

{{ format_instructions }}
"""
