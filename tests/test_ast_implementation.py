import ast
import inspect
from typing import Callable, Any
import textwrap

from pytest import approx


class ModifyReturn(ast.NodeTransformer):
    def __init__(self):
        self.temp_var_counter = 0  # To generate unique temp variable names

    def generate_temp_var_name(self):
        self.temp_var_counter += 1
        return f"_temp_return_value_{self.temp_var_counter}"

    def visit_FunctionDef(self, node):
        new_body = []
        for stmt in node.body:
            if isinstance(stmt, ast.Return):
                if isinstance(stmt.value, ast.Name):
                    # Return is directly a variable; just capture locals
                    capture_stmt = ast.parse("captured = locals()").body[0]
                    new_body.append(capture_stmt)
                else:
                    # Return is an expression; capture into a temp variable
                    temp_var_name = self.generate_temp_var_name()
                    assign_temp_var = ast.parse(f"{temp_var_name} = 0").body[
                        0
                    ]  # Placeholder assignment
                    assign_temp_var.value = (
                        stmt.value
                    )  # Replace placeholder with actual return value
                    new_body.append(assign_temp_var)

                    # Update the return statement to return the temp variable
                    stmt.value = ast.Name(id=temp_var_name, ctx=ast.Load())

                    # Capture locals after assigning to temp variable
                    capture_stmt = ast.parse("captured = locals()").body[0]
                    new_body.append(capture_stmt)

                new_return_stmt = ast.copy_location(
                    ast.Return(value=ast.Name(id="captured", ctx=ast.Load())), stmt
                )
                new_body.append(new_return_stmt)
            else:
                new_body.append(stmt)
        node.body = new_body
        return node


def get_local_vars_and_values_with_context(function: Callable, *args, **kwargs) -> dict:
    source = inspect.getsource(function)
    dedented_source = textwrap.dedent(source)

    tree = ast.parse(dedented_source)

    # Apply the modified ModifyReturn class here
    tree = ModifyReturn().visit(tree)
    ast.fix_missing_locations(tree)

    compiled_code = compile(tree, filename="<ast>", mode="exec")
    namespace = {}
    exec(compiled_code, function.__globals__, namespace)

    modified_function = namespace[function.__name__]
    return_values = modified_function(*args, **kwargs)

    return return_values


def calculation_func(f_hv_tot, n_hpf):
    # @@ Fhv = Fhv,tot,bearing / n(HPF) = {f_hv*1000:.2f} kN
    f_hv = f_hv_tot / n_hpf

    return f_hv


def _test_without_introspection():
    assert calculation_func(10000, 2) == approx(5000)


def _test_with_introspection():
    # Test the revised function
    def example_function(x):

        if x < 10:
            y = 20 * x
            return y

        y = x + 1
        z = y * 2
        return z

    # Get local variables and their values for x = 10
    local_vals = get_local_vars_and_values_with_context(example_function, 10)
    assert local_vals == {"x": 10, "y": 11, "z": 22}

    # Get local variables and their values for x = 9
    local_vals = get_local_vars_and_values_with_context(example_function, 9)
    assert local_vals == {"x": 9, "y": 180}
