import re
from typing import List, Callable

from .constants import TMP_RESULT_VAR_NAME

COMMENT_REGEX = re.compile(r"^(\s*)##! (.+)$")
RETURN_REGEX = re.compile(r"^(\s*)return (.+)$")
COMMENT_REPLACER = lambda g: f'{g[0]}{TMP_RESULT_VAR_NAME}.comments.append(f"{g[1]}")'
RETURN_REPLACER = (
    lambda g: f"{g[0]}{TMP_RESULT_VAR_NAME}.result = {g[1]}; return {TMP_RESULT_VAR_NAME}"
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
