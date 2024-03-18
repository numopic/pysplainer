import typst

import tempfile
import os


def typst_compile_text(text: str, *args, **kwargs):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        # Write data to temporary file
        tmp_file.write(text.encode("utf-8"))
        # Get the path of the temporary file
        temp_path = tmp_file.name

    typst.compile(temp_path, *args, **kwargs)
    os.remove(temp_path)
