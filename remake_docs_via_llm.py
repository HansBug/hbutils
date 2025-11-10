"""
Module for automatically generating Python documentation using OpenAI's language models.

This module provides functionality to automatically generate reStructuredText format
documentation (pydoc) for Python code files using OpenAI's API. It processes Python
source files and adds comprehensive docstrings to functions, methods, and classes
while preserving existing comments and code structure.

The module supports:
- Single file documentation generation
- Batch processing of entire directories
- Automatic translation of non-English comments
- Conversion to reStructuredText format
- Type annotation suggestions
"""
import argparse
import glob
import os
import pathlib
from functools import lru_cache

from openai import OpenAI


@lru_cache()
def get_client() -> OpenAI:
    """
    Create and return an OpenAI client instance.

    This function initializes an OpenAI client using environment variables
    for API key and base URL configuration.

    :return: Configured OpenAI client instance.
    :rtype: OpenAI
    :raises KeyError: If required environment variables are not set.

    Example::
        >>> client = get_client()
        >>> # Use client for API calls
    """
    return OpenAI(
        api_key=os.environ['OPENAI_API_KEY'],
        base_url=os.environ['OPENAI_SITE'],
    )


_SYSTEM_PROMPT = """
You are an assistant specialized in writing pydoc for Python code. I will provide Python code, and you need to write pydoc for its functions, methods, etc., then output the complete runnable code containing both the original code and pydoc for me to copy into my project. Do not output any irrelevant content besides this.

**Basic Requirements:**
- Preserve the content of existing docstrings or comments in the original code
- Write pydoc using reStructuredText format
- Add functional analysis for the entire module at the top of the code (using pydocstring format)
- Convert all non-English comments to English
- Analyze the functionality of functions, methods, classes, and modules as much as possible, providing descriptive and usage guidance content

**Format Example:**
```python
def parse_hf_fs_path(path: str) -> HfFileSystemPath:
    \"\"\"
    Parse the huggingface filesystem path.

    :param path: The path to parse.
    :type path: str

    :return: The parsed huggingface filesystem path.
    :rtype: HfFileSystemPath
    :raises ValueError: If this path is invalid.
    
    Example::
        >>> parse_hf_fs_path('xxxxx')  # comment of this line
        output of this line
    \"\"\"
```

**Detailed Requirements:**
1. Translate all non-English comment content to English
2. For existing comments or docs, avoid modifications unless necessary, try to preserve the original text
3. Identify and correct inconsistencies between existing comments/docs and actual code
4. Add typing for function parameters that lack type annotations (if types can be determined from the code)
5. Convert non-reStructuredText format docs to the required format

**Important Note: Please directly output code with pydoc as docstrings, do not output any irrelevant content!**
"""


def _unwrap_python_code(code_output: str) -> str:
    """
    Remove markdown code block wrappers from the output.

    This function strips markdown code fence markers (```) from the beginning
    and end of the code output if they exist.

    :param code_output: The code string potentially wrapped in markdown code blocks.
    :type code_output: str

    :return: The unwrapped code string.
    :rtype: str

    Example::
        >>> _unwrap_python_code('```python\\nprint("hello")\\n```')
        'print("hello")'
    """
    code_output = code_output.strip()
    lines = code_output.splitlines(keepends=False)
    if lines[0].startswith('```') and lines[-1].startswith('```'):
        lines = lines[1:-1]
    return os.linesep.join(lines)


def get_docs(code_text: str) -> str:
    """
    Generate documentation for the provided Python code using OpenAI API.

    This function sends the provided Python code to OpenAI's language model
    and receives back the same code enhanced with comprehensive documentation.

    :param code_text: The Python source code to document.
    :type code_text: str

    :return: The Python code with added documentation.
    :rtype: str
    :raises Exception: If the API call fails or returns invalid response.

    Example::
        >>> code = "def add(a, b):\\n    return a + b"
        >>> documented_code = get_docs(code)
        >>> # documented_code now contains the function with docstrings
    """
    client = get_client()
    response = client.chat.completions.create(
        model=os.environ.get('OPENAI_MODEL_NAME', "claude-sonnet-4-5"),
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": code_text}
        ],
        max_tokens=128000,
        temperature=0.5
    )
    return _unwrap_python_code(response.choices[0].message.content)


def make_doc_for_file(file: str) -> None:
    """
    Generate and write documentation for a single Python file.

    This function reads a Python file, generates documentation for it using
    the OpenAI API, and overwrites the original file with the documented version.

    :param file: Path to the Python file to document.
    :type file: str

    :raises FileNotFoundError: If the specified file does not exist.
    :raises PermissionError: If the file cannot be written to.

    Example::
        >>> make_doc_for_file('my_script.py')
        >>> # my_script.py now contains enhanced documentation
    """
    print(f'Make docs for {file!r} ...')
    new_docs = get_docs(pathlib.Path(file).read_text())
    with open(file, 'w') as f:
        print(new_docs, file=f)


def make_doc_file_directory(directory: str) -> None:
    """
    Generate documentation for all Python files in a directory recursively.

    This function walks through the specified directory and all its subdirectories,
    finding all Python (.py) files and generating documentation for each one.

    :param directory: Path to the directory containing Python files.
    :type directory: str

    :raises FileNotFoundError: If the specified directory does not exist.
    :raises PermissionError: If files cannot be read or written.

    Example::
        >>> make_doc_file_directory('./my_project')
        >>> # All .py files in my_project and subdirectories are now documented
    """
    for file in glob.glob(os.path.join(directory, '**', '*.py'), recursive=True):
        make_doc_for_file(file)


def main():
    """
    Main function to parse command-line arguments and generate documentation.

    This function serves as the entry point for the command-line interface.
    It parses arguments to determine whether to process a single file or
    an entire directory, then calls the appropriate documentation generation
    function.

    :raises FileNotFoundError: If the specified input path does not exist.
    :raises RuntimeError: If the input path is neither a file nor a directory.

    Example::
        >>> # Command line usage:
        >>> # python script.py -i my_file.py
        >>> # python script.py -i ./my_project
    """
    parser = argparse.ArgumentParser(description='Auto create/update docs for file or directory')
    parser.add_argument('-i', '--input', required=True, help='Input code file or directory')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise FileNotFoundError(f'File not found - {args.input!r}.')
    elif os.path.isfile(args.input):
        make_doc_for_file(args.input)
    elif os.path.isdir(args.input):
        make_doc_file_directory(args.input)
    else:
        raise RuntimeError(f'Unknown input - {args.input!r}.')


if __name__ == "__main__":
    main()
