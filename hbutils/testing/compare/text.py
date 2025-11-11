"""
Text alignment utilities for comparing and processing text in unit tests.

This module provides the :class:`TextAligner` class for flexible text comparison and alignment,
particularly useful in unit testing scenarios where text output needs to be validated.
It supports various text preprocessing operations like stripping, dedenting, and line-by-line transformations.
"""

import io
import os
import textwrap
from typing import List, Union, Callable, Optional

__all__ = [
    'TextAligner',
]

from ...design import SingletonMark
from ...string import plural_word

_NOT_GIVEN = SingletonMark('_TextAligner_NOT_GIVEN')


class TextAligner:
    """
    Text aligner for comparing texts in unittest.
    
    This class provides a flexible way to align, transform, and compare text content.
    It supports various preprocessing operations and can be chained for complex transformations.
    """

    def __init__(self, line_rstrip: bool = True, keep_empty_tail: bool = False,
                 text_func: Optional[Callable[[str], str]] = None,
                 line_func: Optional[Callable[[str], str]] = None,
                 ls_func: Optional[Callable[[List[str]], List[str]]] = None):
        """
        Constructor of :class:`TextAligner`.

        :param line_rstrip: Right strip each line, default is ``True``.
        :type line_rstrip: bool
        :param keep_empty_tail: Keep the empty tail of the text, default is ``False``, which means the \
            empty tails will be ignored.
        :type keep_empty_tail: bool
        :param text_func: Function for preprocessing whole text.
        :type text_func: Optional[Callable[[str], str]]
        :param line_func: Function for processing each line.
        :type line_func: Optional[Callable[[str], str]]
        :param ls_func: Function for processing lines list.
        :type ls_func: Optional[Callable[[List[str]], List[str]]]
        """
        self.__line_rstrip = line_rstrip
        self.__keep_empty_tail = keep_empty_tail
        self.__text_func = text_func or (lambda x: x)
        self.__line_func = line_func or (lambda x: x)
        self.__ls_func = ls_func or (lambda x: x)

    def text_trans(self, text_func: Callable[[str], str]) -> 'TextAligner':
        """
        Transformation for the original text.

        :param text_func: New text process function.
        :type text_func: Callable[[str], str]
        :return: A new :class:`TextAligner` object with ``text_func`` process.
        :rtype: TextAligner
        
        Example::
            >>> from hbutils.testing import TextAligner
            >>> text_align = TextAligner()
            >>> new_align = text_align.text_trans(str.upper)
        """
        return self.__class__(
            self.__line_rstrip, self.__keep_empty_tail,
            lambda x: text_func(self.__text_func(x)),
            self.__line_func, self.__ls_func
        )

    def line_map(self, line_func: Callable[[str], str]) -> 'TextAligner':
        """
        Mapping for the text of each line.

        :param line_func: New line process function.
        :type line_func: Callable[[str], str]
        :return: A new :class:`TextAligner` object with ``line_func`` process.
        :rtype: TextAligner
        
        Example::
            >>> from hbutils.testing import TextAligner
            >>> text_align = TextAligner()
            >>> new_align = text_align.line_map(str.strip)
        """
        return self.__class__(
            self.__line_rstrip, self.__keep_empty_tail,
            self.__text_func,
            lambda x: line_func(self.__line_func(x)),
            self.__ls_func,
        )

    def ls_trans(self, ls_func: Callable[[List[str]], List[str]]) -> 'TextAligner':
        """
        Transformation for the separated lines.

        :param ls_func: New lines process function.
        :type ls_func: Callable[[List[str]], List[str]]
        :return: A new :class:`TextAligner` object with ``ls_func`` process.
        :rtype: TextAligner
        
        Example::
            >>> from hbutils.testing import TextAligner
            >>> text_align = TextAligner()
            >>> new_align = text_align.ls_trans(lambda lines: [line for line in lines if line])
        """
        return self.__class__(
            self.__line_rstrip, self.__keep_empty_tail,
            self.__text_func, self.__line_func,
            lambda x: ls_func(self.__ls_func(x)),
        )

    def __getattr__(self, item: str) -> '_StrMethodProxy':
        """
        Append postprocess from :class:`str` of each line.

        :param item: Method name.
        :type item: str
        :return: A proxy object that wraps the string method.
        :rtype: _StrMethodProxy
        :raises AttributeError: If the method is not found in str class.

        Examples::
            >>> from hbutils.testing import TextAligner
            >>> text_align = TextAligner()
            >>> print(text_align.lower().multiple_lines()('''
            ... Python 3.6.5
            ... Hello world!!
            ...   Do not see me like this...
            ... \\n\\n\\t\\n
            ... '''))
            python 3.6.5
            hello world!!
              do not see me like this...
        """
        return _StrMethodProxy(self, item)

    def multiple_lines(self, lstrip: bool = True, dedent: bool = True) -> 'TextAligner':
        """
        Switch to multiple-line mode.

        :param lstrip: Left strip the original text.
        :type lstrip: bool
        :param dedent: Dedent the text.
        :type dedent: bool
        :return: A new :class:`TextAligner` object configured for multiple-line mode.
        :rtype: TextAligner

        Examples::
            >>> from hbutils.testing import TextAligner
            >>> text_align = TextAligner()
            >>> print(text_align.multiple_lines()('''
            ... Python 3.6.5
            ... Hello world!!
            ...   Do not see me like this...
            ... \\n\\n\\t\\n
            ... '''))
            Python 3.6.5
            Hello world!!
              Do not see me like this...

        .. note::
            With :meth:`multiple_lines`, the text's comparison will be compatible with text wrapper.
        """
        align = self
        if dedent:
            align = align.text_trans(textwrap.dedent)
        if lstrip:
            align = align.text_trans(str.lstrip)

        return align

    def _process(self, text: Union[str, List[str]]) -> List[str]:
        """
        Internal method to process text or lines into a list of aligned lines.

        :param text: Original text or lines.
        :type text: Union[str, List[str]]
        :return: List of processed lines.
        :rtype: List[str]
        :raises TypeError: If the content type is invalid.
        """
        if isinstance(text, (list, tuple)):
            return self._process(os.linesep.join(text))
        elif isinstance(text, str):
            if not self.__keep_empty_tail:
                text = text.rstrip()
            text = self.__text_func(text)

            lines = text.splitlines(keepends=False)
            if self.__line_rstrip:
                lines = list(map(str.rstrip, lines))
            lines = list(map(self.__line_func, lines))
            lines = list(self.__ls_func(lines))

            return lines
        else:
            raise TypeError(f'Invalid content type - {text!r}.')

    def splitlines(self, text: Union[str, List[str]]) -> List[str]:
        """
        Transform the original text or lines to list of aligned lines.

        :param text: Original text or lines.
        :type text: Union[str, List[str]]
        :return: List of split lines.
        :rtype: List[str]

        Examples::
            >>> from hbutils.testing import TextAligner
            >>> text_align = TextAligner()
            >>> print(text_align.splitlines('''Python 3.6.5
            ... Hello world!!
            ...   Do not see me like this...
            ... \\n\\n\\t\\n
            ... '''))
            ['Python 3.6.5', 'Hello world!!', '  Do not see me like this...']

            >>> print(text_align.lstrip().splitlines('''Python 3.6.5
            ... Hello world!!
            ...   Do not see me like this...
            ... \\n\\n\\t\\n
            ... '''))
            ['Python 3.6.5', 'Hello world!!', 'Do not see me like this...']
        """
        return self._process(text)

    def __call__(self, text: Union[str, List[str]]) -> str:
        """
        Transform the original text or lines to aligned text.

        :param text: Original text or lines.
        :type text: Union[str, List[str]]
        :return: Aligned text.
        :rtype: str

        Examples::
            >>> from hbutils.testing import TextAligner
            >>> text_align = TextAligner()
            >>> print(text_align('''Python 3.6.5
            ... Hello world!!
            ...   Do not see me like this...
            ... \\n\\n\\t\\n
            ... '''))
            Python 3.6.5
            Hello world!!
              Do not see me like this...

            >>> print(text_align.lstrip()('''Python 3.6.5
            ... Hello world!!
            ...   Do not see me like this...
            ... \\n\\n\\t\\n
            ... '''))
            Python 3.6.5
            Hello world!!
            Do not see me like this...
        """
        return os.linesep.join(self._process(text))

    @staticmethod
    def _eq_compare_message(expect: List[str], actual: List[str], max_diff: int = 3, max_extra: int = 5) -> str:
        """
        Generate comparison message for equal assertion.

        :param expect: Expected lines.
        :type expect: List[str]
        :param actual: Actual lines.
        :type actual: List[str]
        :param max_diff: Maximum number of different lines to show, default is ``3``.
        :type max_diff: int
        :param max_extra: Maximum number of extra lines to show, default is ``5``.
        :type max_extra: int
        :return: Comparison message describing the differences.
        :rtype: str
        """
        if expect == actual:  # pragma: no cover
            return 'No difference found.'
        else:
            with io.StringIO() as sf:
                if len(expect) != len(actual):
                    print(f'{plural_word(len(expect), "line")} expected, '
                          f'but {plural_word(len(actual), "line")} found actually.', file=sf)

                diff_cnt = 0
                for lineno, (eline, aline) in enumerate(zip(expect, actual), start=1):
                    if eline != aline:
                        diff_cnt += 1
                        if max_diff <= 0 or diff_cnt <= max_diff:
                            print(f'Difference found in line {lineno}:', file=sf)
                            print(f'    Expect: {eline}', file=sf)
                            print(f'    Actual: {aline}', file=sf)
                if 0 < max_diff < diff_cnt:
                    print(f'    ... ({plural_word(diff_cnt - max_diff, "more different line")}) ...', file=sf)

                if len(expect) != len(actual):
                    common_length = min(len(expect), len(actual))
                    if len(expect) > common_length:
                        print(f'Another {plural_word(len(expect) - common_length, "extra line")} '
                              f'found in expected lines:', file=sf)
                        extra_lines = expect[common_length:]
                    elif len(actual) > common_length:
                        print(f'Another {plural_word(len(actual) - common_length, "extra line")} '
                              f'found in actual lines:', file=sf)
                        extra_lines = actual[common_length:]

                    if max_extra > 0:
                        elines = extra_lines[:max_extra]
                    else:
                        elines = extra_lines
                    for line in elines:
                        print(f'    | {line}', file=sf)

                    if len(elines) < len(extra_lines):
                        print(f'    ... ({plural_word(len(extra_lines) - len(elines), "more line")}) ...', file=sf)

                return sf.getvalue()

    def assert_equal(self, expect: Union[str, List[str]], actual: Union[str, List[str]],
                     max_diff: int = 3, max_extra: int = 5):
        """
        Assert two string is equal.

        :param expect: Expected text or lines.
        :type expect: Union[str, List[str]]
        :param actual: Actual text or lines.
        :type actual: Union[str, List[str]]
        :param max_diff: Max different lines to show in assertion message, default is ``3``.
        :type max_diff: int
        :param max_extra: Max extra lines to show in assertion message, default is ``5``.
        :type max_extra: int
        :raises AssertionError: If the texts are not equal.

        Examples::
            >>> from hbutils.testing import TextAligner
            >>> text_align = TextAligner()
            >>> text_align.multiple_lines().assert_equal('''Python 3.6.5
            ... Hello world!!
            ...   Do not see me like this...
            ... \\n\\n\\t\\n
            ... ''', '''
            ...         Python 3.6.5
            ...         Hello world!!
            ...           Do not see me like this...
            ... ''')  # this is okay

            >>> text_align.multiple_lines().assert_equal('''Python 3.6.5
            ... Hello world!!
            ...   Do not see me like this...
            ... \\n\\n\\t\\n
            ... ''', '''
            ...         Python 3.6.5
            ...         Hello world!!
            ...         Do not see me like this...
            ... ''')
            AssertionError: Difference found in line 3:
                Expect:   Do not see me like this...
                Actual: Do not see me like this...
        """
        expect, actual = self._process(expect), self._process(actual)
        assert expect == actual, self._eq_compare_message(expect, actual, max_diff, max_extra)

    @staticmethod
    def _ne_compare_message(expect: List[str], actual: List[str]) -> str:
        """
        Generate comparison message for not equal assertion.

        :param expect: Expected lines.
        :type expect: List[str]
        :param actual: Actual lines.
        :type actual: List[str]
        :return: Comparison message.
        :rtype: str
        """
        if expect != actual:  # pragma: no cover
            return 'Difference found in actual text.'
        else:
            return 'Actual text are completely the same as expected one!'

    def assert_not_equal(self, expect: Union[str, List[str]], actual: Union[str, List[str]]):
        """
        Assert two string is not equal, which is similar to :meth:`assert_equal`.

        :param expect: Expected text or lines.
        :type expect: Union[str, List[str]]
        :param actual: Actual text or lines.
        :type actual: Union[str, List[str]]
        :raises AssertionError: If the texts are equal.
        
        Example::
            >>> from hbutils.testing import TextAligner
            >>> text_align = TextAligner()
            >>> text_align.assert_not_equal("Hello", "World")  # this is okay
            >>> text_align.assert_not_equal("Hello", "Hello")  # this will raise AssertionError
        """
        expect, actual = self._process(expect), self._process(actual)
        assert expect != actual, self._ne_compare_message(expect, actual)


class _StrMethodProxy:
    """
    Proxy class for wrapping string methods to be applied to each line in TextAligner.
    
    This class enables dynamic method chaining by proxying string methods
    and applying them line-by-line through the TextAligner.
    """

    def __init__(self, align: TextAligner, name: str):
        """
        Initialize the string method proxy.

        :param align: The TextAligner instance to proxy for.
        :type align: TextAligner
        :param name: The name of the string method to proxy.
        :type name: str
        :raises AttributeError: If the method name is not found in str class.
        """
        self.__align = align
        if hasattr(str, name) and callable(getattr(str, name)):
            self.__func = getattr(str, name)
        else:
            raise AttributeError(f'Attribute {name!r} not found in str.')

    def __call__(self, *args, **kwargs) -> 'TextAligner':
        """
        Apply the proxied string method to each line.

        :param args: Positional arguments to pass to the string method.
        :param kwargs: Keyword arguments to pass to the string method.
        :return: A new TextAligner with the method applied to each line.
        :rtype: TextAligner
        
        Example::
            >>> from hbutils.testing import TextAligner
            >>> text_align = TextAligner()
            >>> new_align = text_align.lower()  # Applies str.lower to each line
        """
        return self.__align.line_map(lambda x: self.__func(x, *args, **kwargs))
