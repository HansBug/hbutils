import pytest

from hbutils.string import plural_form, singular_form, plural_word


@pytest.mark.unittest
class TestStringTemplate:
    def test_plural_form(self):
        assert plural_form('it') == 'they'
        assert plural_form('word') == 'words'
        assert plural_form('woman') == 'women'

    def test_singular_form(self):
        assert singular_form('it') == 'it'
        assert singular_form('they') == 'it'
        assert singular_form('them') == 'it'
        assert singular_form('word') == 'word'
        assert singular_form('these') == 'this'
        assert singular_form('those') == 'that'

    def test_plural_word(self):
        assert plural_word(0, 'word') == '0 words'
        assert plural_word(1, 'word') == '1 word'
        assert plural_word(2, 'word') == '2 words'
        assert plural_word(23489, 'word') == '23489 words'
