import ast
import inspect
import textwrap
import re
from functools import wraps
from typing import List, Callable

from .explainable_result import ExplainableResult

EXPLAINABLE_RESULT_VAR_NAME = "__explainable_result__"
COMMENT_REGEX = re.compile(r"^(\s*)##! (.+)$")
RETURN_REGEX = re.compile(r"^(\s*)return (.+)$")
COMMENT_REPLACER = (
    lambda g: f'{g[0]}{EXPLAINABLE_RESULT_VAR_NAME}.comments.append(f"{g[1]}")'
)
RETURN_REPLACER = (
    lambda g: f"{g[0]}{EXPLAINABLE_RESULT_VAR_NAME}.result = {g[1]}; return {EXPLAINABLE_RESULT_VAR_NAME}"
)


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


def convert_func_to_explainable(func, *args, **kwargs) -> ExplainableResult:
    """This will convert a normal function into one that returns ExplainableResult"""

    source = inspect.getsource(func)
    dedented_source = textwrap.dedent(source)
    code_lines = dedented_source.split("\n")

    # We need to process comments first as string representation since AST ignores comments
    code_lines = regex_process_lines(code_lines, COMMENT_REGEX, COMMENT_REPLACER)

    # Modify return statements is simpler to do in pure string representation than in AST
    code_lines = regex_process_lines(code_lines, RETURN_REGEX, RETURN_REPLACER)

    if code_lines[0].startswith("@explainable"):
        code_lines = code_lines[1:]

    tree = ast.parse("\n".join(code_lines))

    new_stmt = ast.parse(
        f"__explainable_result__ = ExplainableResult(function_name='{func.__name__}')"
    ).body[0]

    # Modify the AST: Insert the new statement at the beginning of the function body
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            node.body.insert(0, new_stmt)
            break

    recompiled_code = compile(tree, filename="<ast>", mode="exec")

    # Prepare global and local namespace
    func.__globals__["ExplainableResult"] = ExplainableResult
    local_namespace = {}

    # Execute the modified function code in the local namespace
    exec(recompiled_code, func.__globals__, local_namespace)

    wrapped_func = local_namespace[func.__name__]
    result = wrapped_func(*args, **kwargs)
    return result


def explainable(func: Callable) -> Callable:
    """Main Pysplainer decorator"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if "explainable" in kwargs and kwargs["explainable"] == True:
            del kwargs["explainable"]
            return convert_func_to_explainable(func, *args, **kwargs)

        return func(*args, **kwargs)

    return wrapper
