import inspect
import textwrap
import re
from typing import List, Optional, Any

from pydantic import BaseModel, Field


class ExplainableResult(BaseModel):
    result: Optional[Any] = None
    computable_comments: List[str] = Field(default_factory=list)


def modify_statement_for_tracing(line):
    pattern_return = r"^(\s*)return (.+)$"
    match_return = re.match(pattern_return, line)
    pattern_comment = r"^(\s*)##\$ (.+)$"
    match_comment = re.match(pattern_comment, line)
    if match_return:
        whitespace, return_expression = match_return.groups()
        modified_line = f"{whitespace}__tracer_result__.result = {return_expression}; return __tracer_result__"
        return modified_line
    elif match_comment:
        whitespace, comment_expression = match_comment.groups()
        modified_line = f'{whitespace}__tracer_result__.computable_comments.append(f"{comment_expression}")'
        return modified_line

    else:
        # If the pattern does not match, return the unmodified line
        return line


def trace_function(func, *args, **kwargs):
    source = inspect.getsource(func)
    dedented_source = textwrap.dedent(source)
    lines = dedented_source.split("\n")

    # TODO: This does not work if def line has multiple rows or if
    # decorator line is more complex or if there is a docstring
    if lines[0].startswith("def") and lines[0].endswith(":"):
        idx_start = 1
    elif (
        lines[0].startswith("@explainable")
        and lines[1].startswith("def")
        and lines[1].endswith(":")
    ):
        idx_start = 2
    else:
        raise NotImplementedError(
            "The function definition signature is unexpected -- aborting!"
        )
    lines.insert(idx_start, "    __tracer_result__ = ExplainableResult()")

    modified_lines = []
    for line in lines:
        modified_lines.append(modify_statement_for_tracing(line))

    local_namespace = {}

    # Execute the modified function code in the local namespace
    exec(
        "\n".join(modified_lines),
        {**func.__globals__, "ExplainableResult": ExplainableResult},
        local_namespace,
    )

    wrapped_func = local_namespace[func.__name__]
    result = wrapped_func(*args, **kwargs)
    return result
