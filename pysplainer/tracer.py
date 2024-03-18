import inspect
import textwrap
import re


def modify_statement_for_tracing(line):
    pattern_return = r"^(\s*)return (.+)$"
    match_return = re.match(pattern_return, line)
    pattern_comment = r"^(\s*)##\$ (.+)$"
    match_comment = re.match(pattern_comment, line)
    if match_return:
        whitespace, return_expression = match_return.groups()
        modified_line = f"{whitespace}return __traced_lines__, {return_expression}"
        return modified_line
    elif match_comment:
        whitespace, comment_expression = match_comment.groups()
        modified_line = f'{whitespace}__traced_lines__.append(f"{comment_expression}")'
        return modified_line

    else:
        # If the pattern does not match, return the unmodified line
        return line


def trace_function(func, *args, **kwargs):
    source = inspect.getsource(func)
    dedented_source = textwrap.dedent(source)
    lines = dedented_source.split("\n")

    # TODO: This does not work if def line has multiple rows or if there is a docstring
    lines.insert(1, "    __traced_lines__ = []")

    modified_lines = []
    for line in lines:
        modified_lines.append(modify_statement_for_tracing(line))

    local_namespace = {}

    # Execute the modified function code in the local namespace
    exec("\n".join(modified_lines), func.__globals__, local_namespace)

    wrapped_func = local_namespace[func.__name__]
    result = wrapped_func(*args, **kwargs)
    return result
