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

    def test_plural_word(self):
        assert plural_word(0, 'word') == '0 words'
        assert plural_word(1, 'word') == '1 word'
        assert plural_word(2, 'word') == '2 words'
        assert plural_word(23489, 'word') == '23489 words'

        assert plural_word(0, 'word', num_text=True) == 'zero words'
        assert plural_word(1, 'word', num_text=True) == 'one word'
        assert plural_word(2, 'word', num_text=True) == 'two words'
        assert plural_word(23489, 'word', num_text=True) == 'twenty-three thousand, four hundred and eighty-nine words'

        assert plural_word(0, 'word', num_text=True, num_threshold=20) == 'zero words'
        assert plural_word(1, 'word', num_text=True, num_threshold=20) == 'one word'
        assert plural_word(2, 'word', num_text=True, num_threshold=20) == 'two words'
        assert plural_word(23489, 'word', num_text=True, num_threshold=20) == '23,489 words'

        with pytest.warns(UserWarning):
            assert plural_word(0, 'word', num_threshold=20) == '0 words'
        with pytest.warns(UserWarning):
            assert plural_word(1, 'word', num_threshold=20) == '1 word'
        with pytest.warns(UserWarning):
            assert plural_word(2, 'word', num_threshold=20) == '2 words'
        with pytest.warns(UserWarning):
            assert plural_word(23489, 'word', num_threshold=20) == '23489 words'
