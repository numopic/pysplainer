import ast
from typing import Dict, Callable

from .constants import NESTED_FUNC_COMMENTS_KWARG, TMP_RESULT_VAR_NAME, FUNC_ATTR_ID


class AppendKeywordArgumentTransformer(ast.NodeTransformer):

    def __init__(self, global_funcs: Dict[str, Callable], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._global_funcs = global_funcs

    def visit_Call(self, node):
        if (
            isinstance(node.func, ast.Name)
            and node.func.id in self._global_funcs
            and getattr(self._global_funcs[node.func.id], FUNC_ATTR_ID, False)
        ):
            # Append the keyword argument
            new_keyword = ast.keyword(
                arg=NESTED_FUNC_COMMENTS_KWARG,
                value=ast.Attribute(
                    value=ast.Name(id=TMP_RESULT_VAR_NAME, ctx=ast.Load()),
                    attr="comments",
                    ctx=ast.Load(),
                ),
            )
            node.keywords.append(new_keyword)

        # Continue to do the default action for this node, which includes visiting its children
        return self.generic_visit(node)
