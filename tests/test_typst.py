from pysplainer.typst_compile import typst_compile_text

TEXT = """The flow rate of a glacier is
defined by the following equation:

$ Q = rho A v + C $
"""


def test_typst():
    typst_compile_text(TEXT, output="tests/.temp_output/hello2.pdf")
