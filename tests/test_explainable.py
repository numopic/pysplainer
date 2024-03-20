import base64
import os

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

#figure(
    image.decode(
        base64.decode("{img_str}"),
        format: "png",
        width: 5cm,
    ),
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


def test_explainable_trace_to_pdf():
    result = example_function(2, 3, 4, explain=True)
    assert result.result == 22
    from timeit import default_timer as timer

    file_path = "tests/.temp_output/test_explainable_trace_to_pdf.pdf"
    if os.path.exists(file_path):
        os.remove(file_path)
    result.as_pdf(template=TEMPLATE, output=file_path)

    assert os.path.exists(file_path)
