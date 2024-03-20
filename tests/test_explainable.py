from pysplainer import explainable


@explainable
def example_function(x: float, y: float, z: float) -> float:
    ##! This is a printed-out comment
    result = x * y + z**2
    ##! $gamma = x*y + z^2 = {result*1000:.1f}$ mm
    return result


def test_explainable_direct_call():
    result = example_function(2, 3, 4)
    assert result == 22


def test_explainable_call_with_trace():
    result = example_function(2, 3, 4, explain=True)
    assert result.result == 22
    assert result.computable_comments == [
        "This is a printed-out comment",
        "$gamma = x*y + z^2 = 22000.0$ mm",
    ]
