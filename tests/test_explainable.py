import base64
import os

from numpy import ndarray, array, identity
from pytest import approx

from pysplainer import explainable


with open("tests/data/space_invader.png", "rb") as file_handle:
    img_str = base64.b64encode(file_handle.read()).decode("utf-8")

TEMPLATE = f"""
#import "@preview/based:0.1.0": base64

#let title = [Calculation example]
#set page(
  header: align(
    right + horizon,
    title
  ),
)
#align(center, text(17pt)[
  *#title*
])

= Introduction
#lorem(90)

#let space_invader_img = image.decode(
    base64.decode("{img_str}"),
    format: "png",
    width: 5cm,
)
#figure(
    space_invader_img,
    caption: [
        Reading images as base64 technically works fine,
        but it's really slow since the image is first converted to base64, then injected into SVG, 
        then SVG is re-rendered as an image and then it's all scaled and positioned. 
        So many unnecessary steps just for programming conevenience
    ],
)

== Motivation
#lorem(140)

== Problem Statement
#lorem(50)

= Calculation
"""


@explainable
def example_function(x: float, y: float, z: float) -> float:
    ##! This is a printed-out comment
    result = x * y + z**2
    ##! $gamma = x*y + z^2 = {result*1000:.1f}$ mm
    return result


@explainable
def example_function_with_quotes(x: float, y: float, z: float) -> float:
    ##! This is a printed-out "comment"
    result = x * y + z**2
    ##! $gamma = x*y + z^2 = {result*1000:.1f}$ "mm"
    ##! $gamma = x*y + z^2 = {result*1000:.1f}$ \"mm\" but it should also work with backslashes
    return result


def to_typst_2d_mat_str(a: ndarray) -> str:
    return "; ".join([", ".join([str(el) for el in row]) for row in a])


@explainable
def example_matrix_function(a: ndarray, b: ndarray) -> ndarray:
    ##! Inside the explainable function we can do different things that are not necessarily linked to the output.
    ##! $ sum_(k=0)^n k &= 1 + ... + n \\ &= (n(n+1)) / 2 $

    ##! #set math.equation(numbering: \"(1)\")
    ##! $ a = mat(delim: \"[\", {to_typst_2d_mat_str(a)}) $ <eq:a>
    ##! $ b = mat(delim: \"[\", {to_typst_2d_mat_str(b)}) $ <eq:b>
    c = a @ b
    ##! We can see that if we multiply $a$ @eq:a and identity matrix $b$ @eq:b that matrix product does not change
    ##! $ c = a times b = mat(delim: \"[\", {to_typst_2d_mat_str(c)}) $

    return c


@explainable
def example_with_image_in_workdir(x: float) -> float:
    ##! This is a printed-out comment
    result = x**2
    ##! #figure(caption: [This is an image in workdir], image("space_invader.png", width: 5cm))
    return result


def test_explainable_direct_call():
    result = example_function(2, 3, 4)
    assert result == 22


def test_explainable_with_quotes_direct_call():
    result = example_function_with_quotes(2, 3, 4)
    assert result == 22


def test_explainable_call_with_trace():
    result = example_function(2, 3, 4, explainable=True)
    assert result.result == 22
    assert result.comments == [
        "This is a printed-out comment",
        "$gamma = x*y + z^2 = 22000.0$ mm",
    ]


def test_explainable_with_quotes_call_with_trace():
    result = example_function_with_quotes(2, 3, 4, explainable=True)
    assert result.result == 22
    assert result.comments == [
        'This is a printed-out "comment"',
        '$gamma = x*y + z^2 = 22000.0$ "mm"',
        '$gamma = x*y + z^2 = 22000.0$ "mm" but it should also work with backslashes',
    ]


def test_explainable_trace_to_pdf():
    result = example_function(2, 3, 4, explainable=True)
    assert result.result == 22

    file_path = "tests/.temp_output/test_explainable_trace_to_pdf.pdf"
    if os.path.exists(file_path):
        os.remove(file_path)
    result.as_pdf(template=TEMPLATE, output=file_path)

    assert os.path.exists(file_path)


def test_explainable_with_matrices():
    a = array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    b = identity(3)
    result = example_matrix_function(a, b, explainable=True)
    file_path = "tests/.temp_output/test_explainable_matrix.pdf"
    if os.path.exists(file_path):
        os.remove(file_path)
    result.as_pdf(output=file_path)

    assert os.path.exists(file_path)


@explainable
def get_area_square(a: float, b: float) -> float:
    ##! We are calculating the area of a rectangular cross-section:
    area = a * b
    ##! $ A = a times b = {a*1000:.1f} text(\"mm\") times {b*1000:.1f} text(\"mm\") = {area*1e6:.1f} text(\" mm\")^2 $
    return area


@explainable
def get_stress(a: float, b: float, load: float) -> float:
    ##! The following is just calculating with random values and checking if function call without returning values will be picked up:
    get_area_square(0.001, 0.002)

    ##! Now we get to the real values used in the calculation:
    area = get_area_square(a, b)
    # area = get_area_square(
    #     a, b, __explainable_extend_comments__=__explainable_result__.comments
    # )

    ##! We are calculating the stress from load and area:
    sigma = load / area
    ##! $ sigma = F/A = ({load:.1f} text(N)) / ({area*1e6:.1f} text(\" mm\")^2) = {sigma:.1f} text(N)/text(m)^2 $
    return sigma


def test_explainable_with_nested_functions():

    result = get_stress(0.2, 0.15, 2000, explainable=True)
    file_path = "tests/.temp_output/test_nested_functions.pdf"
    if os.path.exists(file_path):
        os.remove(file_path)
    result.as_pdf(output=file_path)

    assert os.path.exists(file_path)


def test_explainable_triangle_metrics():
    @explainable
    def triangle_metrics(x1, y1, x2, y2, x3, y3):
        ##! We have points in 2D plane as $bold(p) = vec(x, y)$
        ##! $ bold(p_1) = vec({x1:.1f}, {y1:.1f}), quad bold(p_2) = vec({x2:.1f}, {y2:.1f}), quad bold(p_3) = vec({x3:.1f}, {y3:.1f}) $
        ##! Calculate the area of the triangle by Heron's formula
        area = abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2)
        ##! $ A = abs((x_1(y_2 - y_3) + x_2(y_3 - y_1) + x_3(y_1 - y_2)) / 2) = {area:.2f} $

        ##! Calculate the lengths of the sides
        side1 = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        ##! $ s_1 = sqrt((x_2 - x_1)^2 + (y_2 - y_1)^2) = {side1:.2f} $
        side2 = ((x3 - x2) ** 2 + (y3 - y2) ** 2) ** 0.5
        ##! $ s_2 = sqrt((x_3 - x_2)^2 + (y_3 - y_2)^2) = {side2:.2f} $
        side3 = ((x1 - x3) ** 2 + (y1 - y3) ** 2) ** 0.5
        ##! $ s_3 = sqrt((x_1 - x_3)^2 + (y_1 - y_3)^2) = {side3:.2f} $

        ##! Circumference is the sum of side lengths
        circumference = side1 + side2 + side3
        ##! $ S = s_1 + s_2 + s_3 = {circumference:.2f} $

        return area, circumference

    inputs = (0.0, 0.0, -0.2, 3.5, 2.7, 0.1)
    assert triangle_metrics(*inputs) == approx((4.735, 10.67634))

    result = triangle_metrics(*inputs, explainable=True)
    file_path = "tests/.temp_output/test_triangle_metrics.pdf"
    if os.path.exists(file_path):
        os.remove(file_path)
    result.as_pdf(output=file_path)

    assert os.path.exists(file_path)


def test_explainable_with_image_in_workdir():
    result = example_with_image_in_workdir(100, explainable=True)
    file_path = "tests/.temp_output/test_explainable_with_image_in_workdir.pdf"
    if os.path.exists(file_path):
        os.remove(file_path)
    result.as_pdf(output=file_path, workdir="tests/data")

    assert os.path.exists(file_path)
