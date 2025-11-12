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
import io
import os
import pathlib
from functools import lru_cache
from operator import itemgetter
from typing import Optional, Tuple, List

from openai import OpenAI

from hbutils.string import format_tree


@lru_cache()
def get_client() -> OpenAI:
    """
    Create and return an OpenAI client instance.

    This function initializes an OpenAI client using environment variables
    for API key and base URL configuration. The result is cached to avoid
    creating multiple client instances.

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


def get_module_doc_string(code_text: str) -> str:
    """
    Extract the module-level docstring from Python code text.

    This function parses the provided Python code to extract the module-level
    docstring (if present) at the beginning of the file. It handles both
    single-quoted (''') and double-quoted (\"\"\") docstring formats.

    :param code_text: The Python source code text to parse.
    :type code_text: str

    :return: The extracted module docstring, or empty string if not found.
    :rtype: str

    Example::
        >>> code = '\"\"\"Module doc\"\"\"\\nprint("hello")'
        >>> get_module_doc_string(code)
        'Module doc'
    """
    doc_lines = []
    status, prefix = 'idle', None

    for line in code_text.strip().splitlines(keepends=False):
        if status == 'idle' and (line.startswith('\'\'\'') or line.startswith('"""')):
            prefix = line[:3]
            status = 'recording'
            if line[3:]:
                doc_lines.append(line[3:])
        elif status == 'recording':
            if line.endswith(prefix):
                if line[:-3]:
                    doc_lines.append(line[:-3])
                break
            else:
                doc_lines.append(line)

    doc_string = os.linesep.join(doc_lines).strip()
    return doc_string


def get_module_doc_tree(file: str) -> str:
    """
    Generate a documentation tree for all Python modules in the file's directory.

    This function recursively scans the directory containing the specified file
    and extracts module-level docstrings from all Python files found. The result
    is formatted as a text document showing the relative path and docstring for
    each module.

    :param file: Path to a Python file whose directory will be scanned.
    :type file: str

    :return: Formatted text containing all module docstrings in the directory tree.
    :rtype: str

    Example::
        >>> doc_tree = get_module_doc_tree('./my_project/module.py')
        >>> # Returns formatted documentation for all modules in my_project/
    """
    with io.StringIO() as sf:
        for pyfile in glob.glob(os.path.join(os.path.dirname(file), '**', '*.py'), recursive=True):
            print(f'## Module doc of {pyfile} (relative: {os.path.relpath(pyfile, os.path.dirname(file))})', file=sf)
            print(f'', file=sf)
            print(f'{get_module_doc_string(pathlib.Path(pyfile).read_text())}', file=sf)
            print(f'', file=sf)

        return sf.getvalue().strip()


def build_file_tree(root_path: str) -> Tuple[str, List]:
    """
    Build a tree structure of all .py files under the given path.

    This function recursively scans the directory structure starting from
    root_path and creates a nested tree representation of all Python files
    and directories containing Python files.

    :param root_path: Root directory path to scan.
    :type root_path: str

    :return: A tuple containing the root path name and its children tree structure.
    :rtype: Tuple[str, List]

    Example::
        >>> tree = build_file_tree('./my_project')
        >>> # Returns ('my_project', [('module.py', []), ('subdir', [...])])
    """
    root_path = pathlib.Path(root_path)

    def build_node(path):
        """
        Recursively build tree nodes.

        :param path: Current path to process.
        :type path: pathlib.Path

        :return: Tuple of (name, children) or None if not a Python file/directory.
        :rtype: Optional[Tuple[str, List]]
        """
        if path.is_file() and path.suffix == '.py':
            return path.name, []
        elif path.is_dir():
            children = []
            try:
                # Get all items in the directory
                for item in sorted(path.iterdir()):
                    if item.is_file() and item.suffix == '.py':
                        children.append((item.name, []))
                    elif item.is_dir():
                        # Recursively check if subdirectory contains .py files
                        sub_node = build_node(item)
                        if sub_node[1]:  # If subdirectory has content
                            children.append(sub_node)
                return path.name, children
            except PermissionError:
                return f"{path.name} (Permission Denied)", []
        return None

    nx = build_node(root_path)
    return os.path.relpath(os.path.normpath(str(root_path)), os.path.abspath('.')), nx[1]


def dir_tree_text(root_path: str, encoding: Optional[str] = None) -> str:
    """
    Display the tree structure of all .py files under the given path as text.

    This function generates a formatted text representation of the directory
    tree containing Python files, suitable for display or logging.

    :param root_path: Root directory path to scan.
    :type root_path: str
    :param encoding: Encoding format, defaults to None (uses system default encoding).
    :type encoding: Optional[str]

    :return: Formatted tree structure as a string.
    :rtype: str

    Example::
        >>> tree_text = dir_tree_text('./my_project')
        >>> print(tree_text)
        my_project
        ├── __init__.py
        ├── module.py
        └── subdir
            └── another.py
    """
    return format_tree(
        node=build_file_tree(root_path),
        format_node=itemgetter(0),
        get_children=itemgetter(1),
        encoding=encoding
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
    and end of the code output if they exist. It handles both generic and
    language-specific code fences.

    :param code_output: The code string potentially wrapped in markdown code blocks.
    :type code_output: str

    :return: The unwrapped code string.
    :rtype: str

    Example::
        >>> _unwrap_python_code('```python\\nprint("hello")\\n```')
        'print("hello")'
        >>> _unwrap_python_code('print("hello")')
        'print("hello")'
    """
    code_output = code_output.strip()
    lines = code_output.splitlines(keepends=False)
    if lines[0].startswith('```') and lines[-1].startswith('```'):
        lines = lines[1:-1]
    return os.linesep.join(lines)


def get_docs(code_text: str, directory_tree: Optional[str] = None, doc_tree: Optional[str] = None) -> str:
    """
    Generate documentation for the provided Python code using OpenAI API.

    This function sends the provided Python code to OpenAI's language model
    and receives back the same code enhanced with comprehensive documentation.
    Optionally includes directory tree context and module documentation tree
    to help the model understand the project structure and existing documentation.

    :param code_text: The Python source code to document.
    :type code_text: str
    :param directory_tree: Optional directory tree structure for context.
    :type directory_tree: Optional[str]
    :param doc_tree: Optional documentation tree of related modules for context.
    :type doc_tree: Optional[str]

    :return: The Python code with added documentation.
    :rtype: str
    :raises Exception: If the API call fails or returns invalid response.

    Example::
        >>> code = "def add(a, b):\\n    return a + b"
        >>> documented_code = get_docs(code)
        >>> # documented_code now contains the function with docstrings
    """
    client = get_client()
    if directory_tree:
        code_text = (f'{code_text}\n\n'
                     f'And this is the directory tree related to this file, you can use it as reference:\n{directory_tree}\n\n')
    if doc_tree:
        code_text = f'{code_text}\n\nAnd this is this docs of the source files in its directory:\n{doc_tree}\n\n'

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


def make_doc_for_file(file: str, include_directory_tree: Optional[bool] = None) -> None:
    """
    Generate and write documentation for a single Python file.

    This function reads a Python file, generates documentation for it using
    the OpenAI API, and overwrites the original file with the documented version.
    For __init__.py files, the directory tree is automatically included as context
    unless explicitly disabled.

    :param file: Path to the Python file to document.
    :type file: str
    :param include_directory_tree: Whether to include directory tree as context.
                                   Defaults to True for __init__.py, False otherwise.
    :type include_directory_tree: Optional[bool]

    :raises FileNotFoundError: If the specified file does not exist.
    :raises PermissionError: If the file cannot be written to.

    Example::
        >>> make_doc_for_file('my_script.py')
        Make docs for 'my_script.py' ...
        >>> # my_script.py now contains enhanced documentation
    """
    if include_directory_tree is None:
        include_directory_tree = os.path.basename(file) == '__init__.py'

    print(f'Make docs for {file!r} ...')
    new_docs = get_docs(
        code_text=pathlib.Path(file).read_text(),
        directory_tree=dir_tree_text(os.path.dirname(file)) if include_directory_tree else None,
        doc_tree=get_module_doc_tree(file) if include_directory_tree else None,
    )
    with open(file, 'w') as f:
        print(new_docs, file=f)


def make_doc_file_directory(directory: str) -> None:
    """
    Generate documentation for all Python files in a directory recursively.

    This function walks through the specified directory and all its subdirectories,
    finding all Python (.py) files and generating documentation for each one.
    The process is performed recursively, documenting all Python files in the
    entire directory tree.

    :param directory: Path to the directory containing Python files.
    :type directory: str

    :raises FileNotFoundError: If the specified directory does not exist.
    :raises PermissionError: If files cannot be read or written.

    Example::
        >>> make_doc_file_directory('./my_project')
        Make docs for './my_project/module.py' ...
        Make docs for './my_project/subdir/another.py' ...
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
