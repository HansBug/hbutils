import pytest

from hbutils.string import camelize, dasherize, humanize, ordinal, ordinalize, parameterize, pluralize, singularize, \
    tableize, titleize, underscore
from hbutils.string.inflection import UNCOUNTABLES

SINGULAR_TO_PLURAL = (
    ("search", "searches"),
    ("switch", "switches"),
    ("fix", "fixes"),
    ("box", "boxes"),
    ("process", "processes"),
    ("address", "addresses"),
    ("case", "cases"),
    ("stack", "stacks"),
    ("wish", "wishes"),
    ("fish", "fish"),
    ("jeans", "jeans"),
    ("funky jeans", "funky jeans"),

    ("category", "categories"),
    ("query", "queries"),
    ("ability", "abilities"),
    ("agency", "agencies"),
    ("movie", "movies"),

    ("archive", "archives"),

    ("index", "indices"),

    ("wife", "wives"),
    ("safe", "saves"),
    ("half", "halves"),

    ("move", "moves"),

    ("salesperson", "salespeople"),
    ("person", "people"),

    ("spokesman", "spokesmen"),
    ("man", "men"),
    ("woman", "women"),

    ("basis", "bases"),
    ("diagnosis", "diagnoses"),
    ("diagnosis_a", "diagnosis_as"),

    ("datum", "data"),
    ("medium", "media"),
    ("stadium", "stadia"),
    ("analysis", "analyses"),

    ("node_child", "node_children"),
    ("child", "children"),

    ("experience", "experiences"),
    ("day", "days"),

    ("comment", "comments"),
    ("foobar", "foobars"),
    ("newsletter", "newsletters"),

    ("old_news", "old_news"),
    ("news", "news"),

    ("series", "series"),
    ("species", "species"),

    ("quiz", "quizzes"),

    ("perspective", "perspectives"),

    ("ox", "oxen"),
    ("passerby", "passersby"),
    ("photo", "photos"),
    ("buffalo", "buffaloes"),
    ("tomato", "tomatoes"),
    ("potato", "potatoes"),
    ("dwarf", "dwarves"),
    ("elf", "elves"),
    ("information", "information"),
    ("equipment", "equipment"),
    ("bus", "buses"),
    ("status", "statuses"),
    ("status_code", "status_codes"),
    ("mouse", "mice"),

    ("louse", "lice"),
    ("house", "houses"),
    ("octopus", "octopi"),
    ("virus", "viri"),
    ("alias", "aliases"),
    ("portfolio", "portfolios"),

    ("vertex", "vertices"),
    ("matrix", "matrices"),
    ("matrix_fu", "matrix_fus"),

    ("axis", "axes"),
    ("testis", "testes"),
    ("crisis", "crises"),

    ("rice", "rice"),
    ("shoe", "shoes"),

    ("horse", "horses"),
    ("prize", "prizes"),
    ("edge", "edges"),

    ("cow", "kine"),
    ("database", "databases"),
    ("human", "humans")
)

CAMEL_TO_UNDERSCORE = (
    ("Product", "product"),
    ("SpecialGuest", "special_guest"),
    ("ApplicationController", "application_controller"),
    ("Area51Controller", "area51_controller"),
)

CAMEL_TO_UNDERSCORE_WITHOUT_REVERSE = (
    ("HTMLTidy", "html_tidy"),
    ("HTMLTidyGenerator", "html_tidy_generator"),
    ("FreeBSD", "free_bsd"),
    ("HTML", "html"),
)

STRING_TO_PARAMETERIZED = (
    (u"Donald E. Knuth", "donald-e-knuth"),
    (
        u"Random text with *(bad)* characters",
        "random-text-with-bad-characters"
    ),
    (u"Allow_Under_Scores", "allow_under_scores"),
    (u"Trailing bad characters!@#", "trailing-bad-characters"),
    (u"!@#Leading bad characters", "leading-bad-characters"),
    (u"Squeeze   separators", "squeeze-separators"),
    (u"Test with + sign", "test-with-sign"),
    (u"Test with malformed utf8 \251", "test-with-malformed-utf8"),
)

STRING_TO_PARAMETERIZE_WITH_NO_SEPARATOR = (
    (u"Donald E. Knuth", "donaldeknuth"),
    (u"With-some-dashes", "with-some-dashes"),
    (u"Random text with *(bad)* characters", "randomtextwithbadcharacters"),
    (u"Trailing bad characters!@#", "trailingbadcharacters"),
    (u"!@#Leading bad characters", "leadingbadcharacters"),
    (u"Squeeze   separators", "squeezeseparators"),
    (u"Test with + sign", "testwithsign"),
    (u"Test with malformed utf8 \251", "testwithmalformedutf8"),
)

STRING_TO_PARAMETERIZE_WITH_UNDERSCORE = (
    (u"Donald E. Knuth", "donald_e_knuth"),
    (
        u"Random text with *(bad)* characters",
        "random_text_with_bad_characters"
    ),
    (u"With-some-dashes", "with-some-dashes"),
    (u"Retain_underscore", "retain_underscore"),
    (u"Trailing bad characters!@#", "trailing_bad_characters"),
    (u"!@#Leading bad characters", "leading_bad_characters"),
    (u"Squeeze   separators", "squeeze_separators"),
    (u"Test with + sign", "test_with_sign"),
    (u"Test with malformed utf8 \251", "test_with_malformed_utf8"),
)

STRING_TO_PARAMETERIZED_AND_NORMALIZED = (
    (u"Malmö", "malmo"),
    (u"Garçons", "garcons"),
    (u"Ops\331", "opsu"),
    (u"Ærøskøbing", "rskbing"),
    (u"Aßlar", "alar"),
    (u"Japanese: 日本語", "japanese"),
)

UNDERSCORE_TO_HUMAN = (
    ("employee_salary", "Employee salary"),
    ("employee_id", "Employee"),
    ("underground", "Underground"),
)

MIXTURE_TO_TITLEIZED = (
    ('active_record', 'Active Record'),
    ('ActiveRecord', 'Active Record'),
    ('action web service', 'Action Web Service'),
    ('Action Web Service', 'Action Web Service'),
    ('Action web service', 'Action Web Service'),
    ('actionwebservice', 'Actionwebservice'),
    ('Actionwebservice', 'Actionwebservice'),
    ("david's code", "David's Code"),
    ("David's code", "David's Code"),
    ("david's Code", "David's Code"),
    ("ana índia", "Ana Índia"),
    ("Ana Índia", "Ana Índia"),
)

ORDINAL_NUMBERS = (
    ("-1", "-1st"),
    ("-2", "-2nd"),
    ("-3", "-3rd"),
    ("-4", "-4th"),
    ("-5", "-5th"),
    ("-6", "-6th"),
    ("-7", "-7th"),
    ("-8", "-8th"),
    ("-9", "-9th"),
    ("-10", "-10th"),
    ("-11", "-11th"),
    ("-12", "-12th"),
    ("-13", "-13th"),
    ("-14", "-14th"),
    ("-20", "-20th"),
    ("-21", "-21st"),
    ("-22", "-22nd"),
    ("-23", "-23rd"),
    ("-24", "-24th"),
    ("-100", "-100th"),
    ("-101", "-101st"),
    ("-102", "-102nd"),
    ("-103", "-103rd"),
    ("-104", "-104th"),
    ("-110", "-110th"),
    ("-111", "-111th"),
    ("-112", "-112th"),
    ("-113", "-113th"),
    ("-1000", "-1000th"),
    ("-1001", "-1001st"),
    ("0", "0th"),
    ("1", "1st"),
    ("2", "2nd"),
    ("3", "3rd"),
    ("4", "4th"),
    ("5", "5th"),
    ("6", "6th"),
    ("7", "7th"),
    ("8", "8th"),
    ("9", "9th"),
    ("10", "10th"),
    ("11", "11th"),
    ("12", "12th"),
    ("13", "13th"),
    ("14", "14th"),
    ("20", "20th"),
    ("21", "21st"),
    ("22", "22nd"),
    ("23", "23rd"),
    ("24", "24th"),
    ("100", "100th"),
    ("101", "101st"),
    ("102", "102nd"),
    ("103", "103rd"),
    ("104", "104th"),
    ("110", "110th"),
    ("111", "111th"),
    ("112", "112th"),
    ("113", "113th"),
    ("1000", "1000th"),
    ("1001", "1001st"),
)

UNDERSCORES_TO_DASHES = (
    ("street", "street"),
    ("street_address", "street-address"),
    ("person_street_address", "person-street-address"),
)

STRING_TO_TABLEIZE = (
    ("person", "people"),
    ("Country", "countries"),
    ("ChildToy", "child_toys"),
    ("_RecipeIngredient", "_recipe_ingredients"),
)


@pytest.mark.unittest
class TestStringInflectionMigrated:
    def test_pluralize_plurals(self):
        assert "plurals" == pluralize("plurals")
        assert "Plurals" == pluralize("Plurals")

    def test_pluralize_empty_string(self):
        assert "" == pluralize("")

    @pytest.mark.parametrize(
        ("word",),
        [(word,) for word in UNCOUNTABLES]
    )
    def test_uncountability(self, word):
        assert word == singularize(word)
        assert word == pluralize(word)
        assert pluralize(word) == singularize(word)

    def test_uncountable_word_is_not_greedy(self):
        uncountable_word = "ors"
        countable_word = "sponsor"

        UNCOUNTABLES.add(uncountable_word)
        try:
            assert uncountable_word == singularize(uncountable_word)
            assert uncountable_word == pluralize(uncountable_word)
            assert (
                    pluralize(uncountable_word) ==
                    singularize(uncountable_word)
            )

            assert "sponsor" == singularize(countable_word)
            assert "sponsors" == pluralize(countable_word)
            assert (
                    "sponsor" ==
                    singularize(pluralize(countable_word))
            )
        finally:
            UNCOUNTABLES.remove(uncountable_word)

    @pytest.mark.parametrize(("singular", "plural"), SINGULAR_TO_PLURAL)
    def test_pluralize_singular(self, singular, plural):
        assert plural == pluralize(singular)
        assert plural.capitalize() == pluralize(singular.capitalize())

    @pytest.mark.parametrize(("singular", "plural"), SINGULAR_TO_PLURAL)
    def test_singularize_plural(self, singular, plural):
        assert singular == singularize(plural)
        assert singular.capitalize() == singularize(plural.capitalize())

    @pytest.mark.parametrize(("singular", "plural"), SINGULAR_TO_PLURAL)
    def test_pluralize_plural(self, singular, plural):
        assert plural == pluralize(plural)
        assert plural.capitalize() == pluralize(plural.capitalize())

    @pytest.mark.parametrize(("before", "titleized"), MIXTURE_TO_TITLEIZED)
    def test_titleize(self, before, titleized):
        assert titleized == titleize(before)

    @pytest.mark.parametrize(("camel", "underscore"), CAMEL_TO_UNDERSCORE)
    def test_camelize(self, camel, underscore):
        assert camel == camelize(underscore)

    def test_camelize_with_lower_downcases_the_first_letter(self):
        assert 'capital' == camelize('Capital', False)

    def test_camelize_with_underscores(self):
        assert "CamelCase" == camelize('Camel_Case')

    @pytest.mark.parametrize(
        ("camel", "us"),
        CAMEL_TO_UNDERSCORE + CAMEL_TO_UNDERSCORE_WITHOUT_REVERSE
    )
    def test_underscore(self, camel, us):
        assert us == underscore(camel)

    @pytest.mark.parametrize(
        ("some_string", "parameterized_string"),
        STRING_TO_PARAMETERIZED
    )
    def test_parameterize(self, some_string, parameterized_string):
        assert parameterized_string == parameterize(some_string)

    @pytest.mark.parametrize(
        ("some_string", "parameterized_string"),
        STRING_TO_PARAMETERIZED_AND_NORMALIZED
    )
    def test_parameterize_and_normalize(self, some_string, parameterized_string):
        assert parameterized_string == parameterize(some_string)

    @pytest.mark.parametrize(
        ("some_string", "parameterized_string"),
        STRING_TO_PARAMETERIZE_WITH_UNDERSCORE
    )
    def test_parameterize_with_custom_separator(self, some_string, parameterized_string):
        assert parameterized_string == parameterize(some_string, '_')

    @pytest.mark.parametrize(
        ("some_string", "parameterized_string"),
        STRING_TO_PARAMETERIZED
    )
    def test_parameterize_with_multi_character_separator(self,
                                                         some_string,
                                                         parameterized_string
                                                         ):
        assert (
                parameterized_string.replace('-', '__sep__') ==
                parameterize(some_string, '__sep__')
        )

    @pytest.mark.parametrize(
        ("some_string", "parameterized_string"),
        STRING_TO_PARAMETERIZE_WITH_NO_SEPARATOR
    )
    def test_parameterize_with_no_separator(self, some_string, parameterized_string):
        assert parameterized_string == parameterize(some_string, '')

    @pytest.mark.parametrize(("underscore", "human"), UNDERSCORE_TO_HUMAN)
    def test_humanize(self, underscore, human):
        assert human == humanize(underscore)

    @pytest.mark.parametrize(("number", "ordinalized"), ORDINAL_NUMBERS)
    def test_ordinal(self, number, ordinalized):
        assert ordinalized == number + ordinal(number)

    @pytest.mark.parametrize(("number", "ordinalized"), ORDINAL_NUMBERS)
    def test_ordinalize(self, number, ordinalized):
        assert ordinalized == ordinalize(number)

    @pytest.mark.parametrize(("input", "expected"), UNDERSCORES_TO_DASHES)
    def test_dasherize(self, input, expected):
        assert dasherize(input) == expected

    @pytest.mark.parametrize(("string", "tableized"), STRING_TO_TABLEIZE)
    def test_tableize(self, string, tableized):
        assert tableize(string) == tableized


@pytest.mark.unittest
class TestStringOrdinal:
    def test_ordinal(self):
        assert ordinal(1) == 'st'
        assert ordinal(2) == 'nd'
        assert ordinal(3) == 'rd'
        assert ordinal(4) == 'th'
        assert ordinal(10) == 'th'
        assert ordinal(11) == 'th'
        assert ordinal(21) == 'st'
        assert ordinal(1001) == 'st'

    def test_ordinalize(self):
        assert ordinalize(1) == '1st'
        assert ordinalize(2) == '2nd'
        assert ordinalize(3) == '3rd'
        assert ordinalize(4) == '4th'
        assert ordinalize(10) == '10th'
        assert ordinalize(11) == '11th'
        assert ordinalize(21) == '21st'
        assert ordinalize(1001) == '1001st'
