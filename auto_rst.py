"""
This module provides functionality to extract public members (classes, functions, variables) from Python source code
and generate reStructuredText (RST) documentation files for Sphinx.

The module uses AST (Abstract Syntax Tree) parsing to analyze Python code and identify public members,
then generates RST files with appropriate Sphinx directives for documentation generation.
"""

import argparse
import ast
import os
import pathlib
from typing import List, Dict, Any

from natsort import natsorted
from sphinx.util.rst import escape


def rst_to_text(text: str) -> str:
    """
    Escape text for use in reStructuredText format.

    :param text: The text to escape.
    :type text: str

    :return: The escaped text safe for RST.
    :rtype: str
    """
    return escape(text)


class PublicMemberExtractor(ast.NodeVisitor):
    """
    Extract public members (classes, functions, variables) from Python code.

    This class uses AST node visiting to traverse Python code and identify
    public classes, functions, and variables, excluding private and protected members.
    """

    def __init__(self):
        """
        Initialize the PublicMemberExtractor.

        Sets up empty lists to store extracted public classes, functions, and variables.
        """
        self.public_classes = []
        self.public_functions = []
        self.public_variables = []

    @classmethod
    def is_private(cls, name: str) -> bool:
        """
        Determine if a name represents a private member (starts with double underscore).

        :param name: The member name to check.
        :type name: str

        :return: True if the name is private, False otherwise.
        :rtype: bool
        """
        return name.startswith('__') and not (name.startswith('__') and name.endswith('__'))

    @classmethod
    def is_protected(cls, name: str) -> bool:
        """
        Determine if a name represents a protected member (starts with single underscore).

        :param name: The member name to check.
        :type name: str

        :return: True if the name is protected, False otherwise.
        :rtype: bool
        """
        return name.startswith('_') and not name.startswith('__')

    @classmethod
    def is_magic_method(cls, name: str) -> bool:
        """
        Determine if a name represents a magic method (starts and ends with double underscore).

        :param name: The member name to check.
        :type name: str

        :return: True if the name is a magic method, False otherwise.
        :rtype: bool
        """
        return name.startswith('__') and name.endswith('__') and len(name) > 4

    @classmethod
    def is_public_or_magic(cls, name: str) -> bool:
        """
        Determine if a name represents a public member or magic method.

        :param name: The member name to check.
        :type name: str

        :return: True if the name is public or a magic method, False otherwise.
        :rtype: bool
        """
        return not cls.is_private(name) and not cls.is_protected(name) or cls.is_magic_method(name)

    def extract_class_members(self, node: ast.ClassDef) -> Dict[str, Any]:
        """
        Extract public members and magic methods from a class definition.

        :param node: The class definition AST node.
        :type node: ast.ClassDef

        :return: Dictionary containing 'methods' and 'attributes' lists.
        :rtype: Dict[str, Any]
        """
        methods = []
        attributes = []

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if self.is_public_or_magic(item.name):
                    method_info = {
                        'name': item.name,
                        'type': 'method',
                        'args': self.extract_function_args(item),
                        'decorators': [self.get_decorator_name(dec) for dec in item.decorator_list],
                        'docstring': ast.get_docstring(item),
                        'lineno': item.lineno,
                        'is_magic': self.is_magic_method(item.name)
                    }
                    methods.append(method_info)

            elif isinstance(item, ast.Assign):
                # Extract class variables
                for target in item.targets:
                    if isinstance(target, ast.Name) and self.is_public_or_magic(target.id):
                        attr_info = {
                            'name': target.id,
                            'type': 'class_variable',
                            'lineno': item.lineno,
                            'value': self.get_node_source(item.value) if hasattr(item, 'value') else None
                        }
                        attributes.append(attr_info)

            elif isinstance(item, ast.AnnAssign):
                # Extract annotated class variables
                if isinstance(item.target, ast.Name) and self.is_public_or_magic(item.target.id):
                    attr_info = {
                        'name': item.target.id,
                        'type': 'annotated_variable',
                        'annotation': self.get_node_source(item.annotation),
                        'lineno': item.lineno,
                        'value': self.get_node_source(item.value) if item.value else None
                    }
                    attributes.append(attr_info)

        return {
            'methods': methods,
            'attributes': attributes
        }

    def extract_function_args(self, node: ast.FunctionDef) -> List[str]:
        """
        Extract function parameter names.

        :param node: The function definition AST node.
        :type node: ast.FunctionDef

        :return: List of parameter names including *args and **kwargs.
        :rtype: List[str]
        """
        args = []

        # Regular parameters
        for arg in node.args.args:
            args.append(arg.arg)

        # *args
        if node.args.vararg:
            args.append(f"*{node.args.vararg.arg}")

        # **kwargs
        if node.args.kwarg:
            args.append(f"**{node.args.kwarg.arg}")

        return args

    def get_decorator_name(self, decorator) -> str:
        """
        Get the name of a decorator.

        :param decorator: The decorator AST node.

        :return: String representation of the decorator name.
        :rtype: str
        """
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return f"{self.get_node_source(decorator.value)}.{decorator.attr}"
        else:
            return self.get_node_source(decorator)

    def get_node_source(self, node) -> str:
        """
        Get the source code representation of an AST node.

        :param node: The AST node to convert to source code.

        :return: String representation of the node's source code.
        :rtype: str
        """
        try:
            if isinstance(node, ast.Name):
                return node.id
            elif isinstance(node, ast.Constant):
                return repr(node.value)
            elif isinstance(node, ast.Attribute):
                return f"{self.get_node_source(node.value)}.{node.attr}"
            elif isinstance(node, ast.List):
                elements = [self.get_node_source(elt) for elt in node.elts]
                return f"[{', '.join(elements)}]"
            elif isinstance(node, ast.Dict):
                pairs = []
                for k, v in zip(node.keys, node.values):
                    key = self.get_node_source(k) if k else None
                    value = self.get_node_source(v)
                    pairs.append(f"{key}: {value}" if key else f"**{value}")
                return f"{{{', '.join(pairs)}}}"
            else:
                # For complex expressions, return type information
                return f"<{type(node).__name__}>"
        except:
            return "<unknown>"

    def visit_ClassDef(self, node: ast.ClassDef):
        """
        Visit a class definition node.

        :param node: The class definition AST node.
        :type node: ast.ClassDef
        """
        if self.is_public_or_magic(node.name):
            # Only process top-level public classes
            class_info = {
                'name': node.name,
                'type': 'class',
                'bases': [self.get_node_source(base) for base in node.bases],
                'decorators': [self.get_decorator_name(dec) for dec in node.decorator_list],
                'docstring': ast.get_docstring(node),
                'lineno': node.lineno,
                'members': self.extract_class_members(node)
            }
            self.public_classes.append(class_info)

        # Don't recursively visit nested classes

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """
        Visit a function definition node.

        :param node: The function definition AST node.
        :type node: ast.FunctionDef
        """
        if self.is_public_or_magic(node.name):
            # Only process top-level public functions
            func_info = {
                'name': node.name,
                'type': 'function',
                'args': self.extract_function_args(node),
                'decorators': [self.get_decorator_name(dec) for dec in node.decorator_list],
                'docstring': ast.get_docstring(node),
                'lineno': node.lineno,
                'returns': self.get_node_source(node.returns) if node.returns else None
            }
            self.public_functions.append(func_info)

        # self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        """
        Visit an assignment statement (variable definition).

        :param node: The assignment AST node.
        :type node: ast.Assign
        """
        # Only process top-level variables
        for target in node.targets:
            if isinstance(target, ast.Name) and self.is_public_or_magic(target.id):
                var_info = {
                    'name': target.id,
                    'type': 'variable',
                    'lineno': node.lineno,
                    'value': self.get_node_source(node.value)
                }
                self.public_variables.append(var_info)

        # self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign):
        """
        Visit an annotated assignment statement.

        :param node: The annotated assignment AST node.
        :type node: ast.AnnAssign
        """
        if isinstance(node.target, ast.Name) and self.is_public_or_magic(node.target.id):
            var_info = {
                'name': node.target.id,
                'type': 'annotated_variable',
                'annotation': self.get_node_source(node.annotation),
                'lineno': node.lineno,
                'value': self.get_node_source(node.value) if node.value else None
            }
            self.public_variables.append(var_info)

        # self.generic_visit(node)


def extract_public_members(source_code: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Extract public members from Python source code.

    :param source_code: Python source code string.
    :type source_code: str

    :return: Dictionary containing 'classes', 'functions', and 'variables' keys.
    :rtype: Dict[str, List[Dict[str, Any]]]

    Example::
        >>> code = "def public_func(): pass"
        >>> result = extract_public_members(code)
        >>> 'functions' in result
        True
    """
    tree = ast.parse(source_code)
    extractor = PublicMemberExtractor()
    extractor.visit(tree)

    return {
        'classes': extractor.public_classes,
        'functions': extractor.public_functions,
        'variables': extractor.public_variables
    }


def extract_public_members_from_file(file_path: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Extract public members from a Python file.

    :param file_path: Path to the Python file.
    :type file_path: str

    :return: Dictionary containing 'classes', 'functions', and 'variables' keys.
    :rtype: Dict[str, List[Dict[str, Any]]]
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    return extract_public_members(source_code)


def print_extracted_members(f, members: Dict[str, List[Dict[str, Any]]]):
    """
    Print extracted member information in RST format.

    :param f: File object to write to.
    :param members: Dictionary containing extracted members.
    :type members: Dict[str, List[Dict[str, Any]]]
    """

    for var in members['variables']:
        print(f'{rst_to_text(var["name"])}', file=f)
        print(f'-----------------------------------------------------', file=f)
        print(f'', file=f)
        print(f'.. autodata:: {var["name"]}', file=f)
        print(f'', file=f)
        print(f'', file=f)

    for cls in members['classes']:
        print(f'{rst_to_text(cls["name"])}', file=f)
        print(f'-----------------------------------------------------', file=f)
        print(f'', file=f)
        print(f'.. autoclass:: {cls["name"]}', file=f)
        member_names = []
        for method in cls['members']['methods']:
            member_names.append(method['name'])
        for attr in cls['members']['attributes']:
            member_names.append(attr['name'])
        if member_names:
            print(f'    :members: {",".join(member_names)}', file=f)
        print(f'', file=f)
        print(f'', file=f)

    for func in members['functions']:
        print(f'{rst_to_text(func["name"])}', file=f)
        print(f'-----------------------------------------------------', file=f)
        print(f'', file=f)
        print(f'.. autofunction:: {func["name"]}', file=f)
        print(f'', file=f)
        print(f'', file=f)


def convert_code_to_rst(code_file: str, rst_file: str, lib_dir: str = '.'):
    """
    Convert a Python code file to an RST documentation file.

    :param code_file: Path to the Python source code file.
    :type code_file: str
    :param rst_file: Path to the output RST file.
    :type rst_file: str
    :param lib_dir: Base library directory for calculating relative module paths. Defaults to '.'.
    :type lib_dir: str

    Example::
        >>> convert_code_to_rst('mymodule.py', 'docs/mymodule.rst', lib_dir='src')
        # Generates RST documentation for mymodule.py
    """
    if os.path.dirname(rst_file):
        os.makedirs(os.path.dirname(rst_file), exist_ok=True)
    members = extract_public_members(pathlib.Path(code_file).read_text())

    with open(rst_file, 'w') as f:
        rel_file = os.path.relpath(os.path.abspath(code_file), os.path.abspath(lib_dir))
        rel_segs = os.path.splitext(rel_file)[0]
        module_name = rel_segs.replace('/', '.').replace('\\', '.')
        if module_name.split('.')[-1] == '__init__':
            module_name = '.'.join(module_name.split('.')[:-1])

        print(f'{rst_to_text(module_name)}', file=f)
        print(f'========================================================', file=f)
        print(f'', file=f)

        print(f'.. currentmodule:: {module_name}', file=f)
        print(f'', file=f)
        print(f'.. automodule:: {module_name}', file=f)
        print(f'', file=f)
        print(f'', file=f)

        if os.path.basename(code_file) != '__init__.py':
            print_extracted_members(f, members)
        else:
            code_rels = []
            for code_rel_file in os.listdir(os.path.dirname(code_file)):
                code_rel_base = os.path.splitext(code_rel_file)[0]
                code_abs_file = os.path.abspath(os.path.join(os.path.dirname(code_file), code_rel_file))
                if os.path.isfile(code_abs_file) and code_rel_file.endswith('.py') and \
                        not (code_rel_base.startswith('__') and code_rel_base.endswith('__')):
                    code_rels.append(code_rel_base)
                elif os.path.isdir(code_abs_file) and os.path.exists(os.path.join(code_abs_file, '__init__.py')):
                    code_rels.append(f'{code_rel_base}/index')

            if code_rels:
                code_rels = natsorted(code_rels)
                print(f'.. toctree::', file=f)
                print(f'    :maxdepth: 3', file=f)
                print(f'', file=f)
                for code_rel_base in code_rels:
                    print(f'    {code_rel_base}', file=f)
                print(f'', file=f)


def main():
    """
    Main entry point for the command-line interface.

    Parses command-line arguments and converts a Python code file to RST documentation.
    """
    parser = argparse.ArgumentParser(description='Auto create rst docs for python code file')
    parser.add_argument('-i', '--input', required=True, help='Input python code file')
    parser.add_argument('-o', '--output', required=True, help='Output rst doc file')
    args = parser.parse_args()

    convert_code_to_rst(
        code_file=args.input,
        rst_file=args.output,
        lib_dir='.'
    )


if __name__ == "__main__":
    main()
