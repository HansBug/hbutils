import pytest

from hbutils.testing import capture_output, TextAligner


@pytest.fixture()
def complex_print_result():
    with capture_output() as co:
        print(f'Python 3.6.5')
        print('Hello world!!')
        print('  Do not see me like this...')

    return co.stdout


@pytest.fixture()
def text_align():
    return TextAligner().multiple_lines()


@pytest.mark.unittest
class TestTestingCompareText:
    def test_text_approx(self, complex_print_result, text_align):
        text_align.assert_equal("""
            Python 3.6.5
            Hello world!!
              Do not see me like this...

        """, complex_print_result)

        text_align.assert_equal([
            'Python 3.6.5',
            'Hello world!!',
            '  Do not see me like this...',
        ], complex_print_result)

        text_align.assert_not_equal("""
            Python 3.6.5
            Hello world!!
            Do not see me like this...
        """, complex_print_result)

        text_align.assert_not_equal([
            'Python 3.6.5',
            'Hello world!!',
            'Do not see me like this...',
        ], complex_print_result)

    def test_text_approx_splitlines(self, complex_print_result, text_align):
        assert text_align.splitlines(complex_print_result) == [
            'Python 3.6.5',
            'Hello world!!',
            '  Do not see me like this...',
        ]
        assert text_align.lower().lstrip().splitlines(complex_print_result) == [
            'python 3.6.5',
            'hello world!!',
            'do not see me like this...',
        ]

        with pytest.raises(TypeError):
            _ = text_align.splitlines(None)

    def test_text_approx_to_text(self, complex_print_result, text_align):
        assert text_align(complex_print_result).splitlines(keepends=False) == [
            'Python 3.6.5',
            'Hello world!!',
            '  Do not see me like this...',
        ]

        with pytest.raises(TypeError):
            _ = text_align(None)

    def test_text_approx_method(self, complex_print_result, text_align):
        text_align.lstrip().assert_equal("""
            Python 3.6.5
            Hello world!!
              Do not see me like this...

        """, complex_print_result)

        text_align.lstrip().assert_equal("""
            Python 3.6.5
            Hello world!!
            Do not see me like this...
        """, complex_print_result)

        text_align.lstrip().upper().assert_equal("""
            python 3.6.5
            hello world!!
            Do not see me like this...
        """, complex_print_result)

        with pytest.raises(AttributeError):
            _ = text_align.ffff

    def test_eq_message(self, complex_print_result, text_align):
        with pytest.raises(AssertionError) as ei:
            text_align.assert_equal("""
                Python 3.6.5
                Hello world!!
                Do not see me like this...
            """, complex_print_result)
        err = ei.value
        assert isinstance(err, AssertionError)
        msg, = err.args
        assert text_align.splitlines(msg) == [
            'Difference found in line 3:',
            '    Expect: Do not see me like this...',
            '    Actual:   Do not see me like this...',
        ]

        with pytest.raises(AssertionError) as ei:
            text_align.assert_equal("""
                Python 3.6.5
                Hello world!!
                Do not see me like this...

                nihao
                  sdkfjl
                233
                ksdf
                ksdiufl;
                dsafuodes
            """, complex_print_result)
        err = ei.value
        assert isinstance(err, AssertionError)
        msg, = err.args
        assert text_align.splitlines(msg) == [
            '10 lines expected, but 3 lines found actually.',
            'Difference found in line 3:',
            '    Expect: Do not see me like this...',
            '    Actual:   Do not see me like this...',
            'Another 7 extra lines found in expected lines:',
            '    |',
            '    | nihao',
            '    |   sdkfjl',
            '    | 233',
            '    | ksdf',
            '    ... (2 more lines) ...'
        ]

        with pytest.raises(AssertionError) as ei:
            text_align.assert_equal("""
                Python 3.6.f5
                Hello world!!
                Do not see me like this...

                nihao
                  sdkfjl
                233
                ksdf
                ksdiufl;
                dsafuodes
            """, complex_print_result, max_diff=0, max_extra=0)
        err = ei.value
        assert isinstance(err, AssertionError)
        msg, = err.args
        assert text_align.splitlines(msg) == [
            '10 lines expected, but 3 lines found actually.',
            'Difference found in line 1:',
            '    Expect: Python 3.6.f5',
            '    Actual: Python 3.6.5',
            'Difference found in line 3:',
            '    Expect: Do not see me like this...',
            '    Actual:   Do not see me like this...',
            'Another 7 extra lines found in expected lines:',
            '    |',
            '    | nihao',
            '    |   sdkfjl',
            '    | 233',
            '    | ksdf',
            '    | ksdiufl;',
            '    | dsafuodes'
        ]

        with pytest.raises(AssertionError) as ei:
            text_align.assert_equal("""
                Python 3.6.f5
                Hello world!!
                Do not see me like this...

                nihao
                  sdkfjl
                233
                ksdf
                ksdiufl;
                dsafuodes
            """, complex_print_result, max_diff=1, max_extra=1)
        err = ei.value
        assert isinstance(err, AssertionError)
        msg, = err.args
        assert text_align.splitlines(msg) == [
            '10 lines expected, but 3 lines found actually.',
            'Difference found in line 1:',
            '    Expect: Python 3.6.f5',
            '    Actual: Python 3.6.5',
            '    ... (1 more different line) ...',
            'Another 7 extra lines found in expected lines:',
            '    |',
            '    ... (6 more lines) ...',
        ]

        with pytest.raises(AssertionError) as ei:
            text_align.assert_equal("""
                Python 3.6.f5
            """, complex_print_result, max_diff=1, max_extra=1)
        err = ei.value
        assert isinstance(err, AssertionError)
        msg, = err.args
        assert text_align.splitlines(msg) == [
            '1 line expected, but 3 lines found actually.',
            'Difference found in line 1:',
            '    Expect: Python 3.6.f5',
            '    Actual: Python 3.6.5',
            'Another 2 extra lines found in actual lines:',
            '    | Hello world!!',
            '    ... (1 more line) ...',
        ]

    def test_ne_message(self, complex_print_result, text_align):
        with pytest.raises(AssertionError) as ei:
            text_align.assert_not_equal("""
                Python 3.6.5
                Hello world!!
                  Do not see me like this...
            """, complex_print_result)

        err = ei.value
        assert isinstance(err, AssertionError)
        msg, = err.args
        assert text_align.splitlines(msg) == [
            'Actual text are completely the same as expected one!',
        ]

    def test_ls_func(self, complex_print_result, text_align):
        text_align.ls_trans(lambda x: filter(bool, x)).assert_equal("""
            Python 3.6.5

            Hello world!!

              Do not see me like this...
        """, complex_print_result)
