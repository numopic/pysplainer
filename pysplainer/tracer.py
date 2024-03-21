import inspect
import textwrap
import re
from typing import List, Callable

from .explainable_result import ExplainableResult

EXPLAINABLE_RESULT_VAR_NAME = "__explainable_result__"
COMMENT_REGEX = re.compile(r"^(\s*)##! (.+)$")
RETURN_REGEX = re.compile(r"^(\s*)return (.+)$")


def regex_process_lines(
    lines: List[str], compiled_regex: re.Pattern, replacement_func: Callable
) -> List[str]:
    result = []
    for line in lines:
        match_comment = compiled_regex.match(line)
        if not match_comment:
            result.append(line)
            continue

        matched_groups = match_comment.groups()
        modified_line = replacement_func(matched_groups)
        result.append(modified_line)

    return result


def trace_function(func, *args, **kwargs):
    source = inspect.getsource(func)
    dedented_source = textwrap.dedent(source)
    code_lines = dedented_source.split("\n")

    # Processing comments should be done first since it needs to operate on pure string representation of the function
    code_lines = regex_process_lines(
        code_lines,
        COMMENT_REGEX,
        lambda g: f'{g[0]}{EXPLAINABLE_RESULT_VAR_NAME}.comments.append(f"{g[1]}")',
    )

    # Modify return statements
    code_lines = regex_process_lines(
        code_lines,
        RETURN_REGEX,
        lambda g: f"{g[0]}{EXPLAINABLE_RESULT_VAR_NAME}.result = {g[1]}; return {EXPLAINABLE_RESULT_VAR_NAME}",
    )

    if code_lines[0].startswith("@explainable"):
        code_lines = code_lines[1:]

    # TODO: This does not work if def line has multiple rows or if
    # decorator line is more complex or if there is a docstring
    if code_lines[0].startswith("def") and code_lines[0].endswith(":"):
        idx_start = 1
    else:
        raise NotImplementedError(
            "The function definition signature is unexpected -- aborting!"
        )
    code_lines.insert(
        idx_start,
        f'    {EXPLAINABLE_RESULT_VAR_NAME} = ExplainableResult(function_name="{func.__name__}")',
    )

    local_namespace = {}

    # Execute the modified function code in the local namespace
    exec(
        "\n".join(code_lines),
        {**func.__globals__, "ExplainableResult": ExplainableResult},
        local_namespace,
    )

    wrapped_func = local_namespace[func.__name__]
    result = wrapped_func(*args, **kwargs)
    return result
