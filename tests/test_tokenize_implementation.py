import inspect
import tokenize
from io import BytesIO


# Example function to tokenize
def func(x):
    return x + 1


# Get the source code of the function
source_code = inspect.getsource(func)

# Convert the source code string to bytes
source_bytes = source_code.encode("utf-8")

# Tokenize the source code
tokens = tokenize.tokenize(BytesIO(source_bytes).readline)


def test_tokenize():
    for token in tokens:
        print(token)


def test_replace_comments():
    source_code = """
def example_function():
    ##! This is a special comment
    pass
    """

    # Function to replace specific comments with print statements
    def replace_special_comments(code):
        result = []
        tokens = tokenize.tokenize(BytesIO(code.encode("utf-8")).readline)

        for toknum, tokval, start, end, line in tokens:
            if toknum == tokenize.COMMENT and tokval.startswith("##!"):
                # Remove the marker and leading spaces
                special_comment_content = tokval[3:].strip()
                replacement = f"print({special_comment_content})"
                result.append((tokenize.NAME, replacement))
            else:
                result.append((toknum, tokval))

        return tokenize.untokenize(result).decode("utf-8")

    # Use the function on the source code
    modified_code = replace_special_comments(source_code)
    print(modified_code)
