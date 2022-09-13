import io
import os
import textwrap
from typing import List, Union

__all__ = [
    'TextAligner',
]

from ...design import SingletonMark

from ...string import plural_word

_NOT_GIVEN = SingletonMark('_TextAligner_NOT_GIVEN')


class TextAligner:
    def __init__(self, line_rstrip: bool = True, keep_empty_tail: bool = False,
                 text_func=None, line_func=None, ls_func=None):
        self.__line_rstrip = line_rstrip
        self.__keep_empty_tail = keep_empty_tail
        self.__text_func = text_func or (lambda x: x)
        self.__line_func = line_func or (lambda x: x)
        self.__ls_func = ls_func or (lambda x: x)

    def text_trans(self, text_func):
        return self.__class__(
            self.__line_func, self.__keep_empty_tail,
            lambda x: text_func(self.__text_func(x)),
            self.__line_func, self.__ls_func
        )

    def line_map(self, line_func):
        return self.__class__(
            self.__line_func, self.__keep_empty_tail,
            self.__text_func,
            lambda x: line_func(self.__line_func(x)),
            self.__ls_func,
        )

    def ls_trans(self, ls_func):
        return self.__class__(
            self.__line_func, self.__keep_empty_tail,
            self.__text_func, self.__line_func,
            lambda x: ls_func(self.__ls_func(x)),
        )

    def __getattr__(self, item: str) -> '_StrMethodProxy':
        return _StrMethodProxy(self, item)

    def multiple_lines(self, lstrip: bool = True, dedent: bool = True):
        align = self
        if dedent:
            align = align.text_trans(textwrap.dedent)
        if lstrip:
            align = align.text_trans(str.lstrip)

        return align

    def _process(self, text: Union[str, List[str]]) -> List[str]:
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
        return self._process(text)

    def __call__(self, text: Union[str, List[str]]) -> str:
        return os.linesep.join(self._process(text))

    @staticmethod
    def _eq_compare_message(expect: List[str], actual: List[str], max_diff: int = 3, max_extra: int = 5):
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
        expect, actual = self._process(expect), self._process(actual)
        assert expect == actual, self._eq_compare_message(expect, actual, max_diff, max_extra)

    @staticmethod
    def _ne_compare_message(expect: List[str], actual: List[str]):
        if expect != actual:  # pragma: no cover
            return 'Difference found in actual text.'
        else:
            return 'Actual text are completely the same as expected one!'

    def assert_not_equal(self, expect: Union[str, List[str]], actual: Union[str, List[str]]):
        expect, actual = self._process(expect), self._process(actual)
        assert expect != actual, self._ne_compare_message(expect, actual)


class _StrMethodProxy:
    def __init__(self, align: TextAligner, name: str):
        self.__align = align
        if hasattr(str, name) and callable(getattr(str, name)):
            self.__func = getattr(str, name)
        else:
            raise AttributeError(f'Attribute {name!r} not found in str.')

    def __call__(self, *args, **kwargs) -> 'TextAligner':
        return self.__align.line_map(lambda x: self.__func(x, *args, **kwargs))
