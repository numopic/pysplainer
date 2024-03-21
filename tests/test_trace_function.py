from pysplainer import convert_func_to_explainable


def example_function(x):
    if x < 10:
        y = 20 * x
        ##! y = {y / 1000:.2f} kN <eq:y>
        return y
    y = x + 1
    z = y * 2
    ##! y = {y / 1000:.2f} kN <eq:y>
    ##! z = {z / 1000:.2f} kN <eq:z>
    return z


def test_trace_function():
    result = convert_func_to_explainable(example_function, 9)
    assert result.comments == ["y = 0.18 kN <eq:y>"]
    assert result.result == 180

    result = convert_func_to_explainable(example_function, 22)
    assert result.comments == ["y = 0.02 kN <eq:y>", "z = 0.05 kN <eq:z>"]
    assert result.result == 46
    assert result.function_name == "example_function"
