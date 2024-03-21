import base64
import os

from numpy import ndarray, array, identity

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
        Space invaders are objectively the best game and reading images as base64 technically works fine,
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


def test_explainable_direct_call():
    result = example_function(2, 3, 4)
    assert result == 22


def test_explainable_call_with_trace():
    result = example_function(2, 3, 4, explainable=True)
    assert result.result == 22
    assert result.computable_comments == [
        "This is a printed-out comment",
        "$gamma = x*y + z^2 = 22000.0$ mm",
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
