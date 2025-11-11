import os
import re
from codecs import open
from distutils.core import setup

from setuptools import find_packages

_package_name = "hbutils"

here = os.path.abspath(os.path.dirname(__file__))
meta = {}
with open(os.path.join(here, _package_name, 'config', 'meta.py'), 'r', 'utf-8') as f:
    exec(f.read(), meta)


def _load_req(file: str):
    with open(file, 'r', 'utf-8') as f:
        return [line.strip() for line in f.readlines() if line.strip()]


requirements = _load_req('requirements.txt')

_REQ_PATTERN = re.compile('^requirements-([a-zA-Z0-9_]+)\\.txt$')
group_requirements = {
    item.group(1): _load_req(item.group(0))
    for item in [_REQ_PATTERN.fullmatch(reqpath) for reqpath in os.listdir()] if item
}

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    # information
    name=meta['__TITLE__'],
    version=meta['__VERSION__'],
    packages=find_packages(
        include=(_package_name, "%s.*" % _package_name)
    ),
    description=meta['__DESCRIPTION__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=meta['__AUTHOR__'],
    author_email=meta['__AUTHOR_EMAIL__'],
    license='Apache License, Version 2.0',
    keywords='python, generic, utilities, algorithms, data structures, system operations, design patterns, testing tools',
    url='https://github.com/HansBug/hbutils',
    project_urls={
        'Homepage': 'https://github.com/HansBug/hbutils',
        'Documentation': 'https://hbutils.readthedocs.io/en/latest/',
        'Repository': 'https://github.com/HansBug/hbutils',
        'Bug Reports': 'https://github.com/HansBug/hbutils/issues',
        'Source': 'https://github.com/HansBug/hbutils',
    },

    # environment
    python_requires=">=3.8",
    install_requires=requirements,
    tests_require=group_requirements.get('test', []),
    extras_require=group_requirements,
    classifiers=[
        # Development Status
        'Development Status :: 5 - Production/Stable',

        # Intended Audience
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',

        # License
        'License :: OSI Approved :: Apache Software License',

        # Operating System
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',

        # Programming Language
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',

        # Topic
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Topic :: System :: Systems Administration',
        'Topic :: Scientific/Engineering',
        'Topic :: Text Processing',
        'Topic :: Software Development :: Testing',

        # Natural Language
        'Natural Language :: English',

        # Environment
        'Environment :: Console',
        'Environment :: Other Environment',

        # Framework
        'Framework :: Pytest',

        # Typing
        'Typing :: Typed',
    ],
)
