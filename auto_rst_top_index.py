"""
Auto-generate RST documentation top index for Python projects.

This module provides functionality to automatically create a top-level index file
in reStructuredText format for a Python project's API documentation. It scans a
project directory for Python modules and packages, then generates a toctree
directive that can be used in Sphinx documentation.

The generated index includes all Python packages (directories with __init__.py)
and standalone Python modules (excluding __init__.py and other dunder files).
"""

import argparse
import os

from natsort import natsorted


def main():
    """
    Main entry point for the RST documentation index generator.

    This function parses command-line arguments, scans the input directory for
    Python modules and packages, and generates an RST file with a toctree
    directive containing all discovered items in natural sorted order.

    The function identifies:
    - Python packages: directories containing __init__.py
    - Python modules: .py files that don't start with '__'

    Command-line arguments:
        -i, --input_dir: Input Python project directory to scan
        -o, --output: Output RST documentation top index file path

    Example::
        >>> # Command line usage
        >>> python script.py -i ./my_project -o ./docs/index.rst
        # Generates an index.rst file with toctree for all modules in my_project
    """
    parser = argparse.ArgumentParser(description='Auto create rst docs top index for project')
    parser.add_argument('-i', '--input_dir', required=True, help='Input python project directory')
    parser.add_argument('-o', '--output', required=True, help='Output rst doc top index file')
    args = parser.parse_args()

    rel_names = []
    for name in os.listdir(args.input_dir):
        item_path = os.path.join(args.input_dir, name)
        # Check if it's a package (directory with __init__.py) or a standalone module
        if (os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, '__init__.py'))) or \
                (os.path.isfile(item_path) and name.endswith('.py') and not name.startswith('__')):
            if name.endswith('.py'):
                # Remove .py extension for modules
                rel_names.append(os.path.splitext(name)[0])
            else:
                # Keep directory name for packages
                rel_names.append(name)

    # Sort names naturally (e.g., module1, module2, module10)
    rel_names = natsorted(rel_names)
    
    # Write the RST toctree to output file
    with open(args.output, 'w') as f:
        print(f'.. toctree::', file=f)
        print(f'    :maxdepth: 2', file=f)
        print(f'    :caption: API Documentation', file=f)
        print(f'', file=f)
        for name in rel_names:
            # Packages get /index suffix, modules don't
            if os.path.exists(os.path.join(args.input_dir, name, '__init__.py')):
                print(f'    api_doc/{name}/index', file=f)
            else:
                print(f'    api_doc/{name}', file=f)
        print(f'', file=f)


if __name__ == '__main__':
    main()
