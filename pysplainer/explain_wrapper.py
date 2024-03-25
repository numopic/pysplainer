import ast
import inspect
import textwrap
from functools import wraps
from typing import Callable

from .explainable_result import ExplainableResult
from .constants import (
    EXPLAINABLE_TRIGGER_KWARG,
    FUNC_ATTR_ID,
    NESTED_FUNC_COMMENTS_KWARG,
    TMP_RESULT_VAR_NAME,
)
from .explain_regex import (
    COMMENT_REGEX,
    COMMENT_REPLACER,
    RETURN_REGEX,
    RETURN_REPLACER,
    regex_process_lines,
)
from .explain_ast import AppendKeywordArgumentTransformer


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

    # Modify the AST: Insert the new statement at the beginning of the function body
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            new_stmt = ast.parse(
                f"{TMP_RESULT_VAR_NAME} = ExplainableResult(function_name='{func.__name__}')"
            ).body[0]
            node.body.insert(0, new_stmt)
            break

    # Transform the AST for explainable nested functions
    transformer = AppendKeywordArgumentTransformer(func.__globals__)
    modified_tree = transformer.visit(tree)

    ast.fix_missing_locations(modified_tree)
    recompiled_code = compile(modified_tree, filename="<ast>", mode="exec")

    # Prepare global and local namespace
    func.__globals__["ExplainableResult"] = ExplainableResult
    local_namespace = {}

    # Execute the modified function code in the local namespace
    exec(recompiled_code, func.__globals__, local_namespace)

    wrapped_func = local_namespace[func.__name__]
    result = wrapped_func(*args, **kwargs)
    return result


def explainable_extend_comments(func, comments, *args, **kwargs):
    explainable_result = convert_func_to_explainable(func, *args, **kwargs)
    comments.extend(explainable_result.comments)
    return explainable_result.result


def explainable(func: Callable) -> Callable:
    """Main Pysplainer decorator"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if (
            EXPLAINABLE_TRIGGER_KWARG in kwargs
            and kwargs[EXPLAINABLE_TRIGGER_KWARG] == True
        ):
            del kwargs[EXPLAINABLE_TRIGGER_KWARG]
            return convert_func_to_explainable(func, *args, **kwargs)

        elif NESTED_FUNC_COMMENTS_KWARG in kwargs:
            comments_to_extend = kwargs[NESTED_FUNC_COMMENTS_KWARG]
            del kwargs[NESTED_FUNC_COMMENTS_KWARG]
            return explainable_extend_comments(
                func, comments_to_extend, *args, **kwargs
            )

        return func(*args, **kwargs)

    setattr(wrapper, FUNC_ATTR_ID, True)
    return wrapper
