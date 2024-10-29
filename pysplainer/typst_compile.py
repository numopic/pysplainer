from typing import Optional
import uuid
import typst

import tempfile
import os


def typst_compile_text(text: str, workdir: Optional[str] = None, *args, **kwargs):
    # Create a temporary file
    if workdir:
        temp_path = f"{workdir}/__temp__{uuid.uuid4()}.typ"
        with open(temp_path, "wt", encoding="utf-8") as file_handle:
            file_handle.write(text)
    else:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            # Write data to temporary file
            tmp_file.write(text.encode("utf-8"))
            # Get the path of the temporary file
            temp_path = tmp_file.name

    try:
        result = typst.compile(temp_path, *args, **kwargs)
    finally:
        os.remove(temp_path)

    return result
