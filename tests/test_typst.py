import os

from pysplainer.typst_compile import typst_compile_text

TEXT = """The flow rate of a glacier is
defined by the following equation:

$ Q = rho A v + C $
"""


def test_typst():
    file_path = "tests/.temp_output/hello2.pdf"

    if os.path.exists(file_path):
        os.remove(file_path)
    typst_compile_text(TEXT, output=file_path)

    assert os.path.exists(file_path)
