"""
Overview:
    This module provides useful utilities for word inflections, including functions for pluralization,
    singularization, camelization, and other string transformations. It is extended based on the
    `jpvanhal/inflection <https://github.com/jpvanhal/inflection>`_ library.

Functions:
    - camelize: Convert strings to CamelCase.
    - dasherize: Replace underscores with dashes in the string.
    - humanize: Capitalize the first word and turn underscores into spaces.
    - ordinal: Return the suffix for ordinal numbers.
    - ordinalize: Turn a number into an ordinal string.
    - parameterize: Replace special characters in a string for URL-friendly format.
    - pluralize: Return the plural form of a word.
    - singularize: Return the singular form of a word.
    - tableize: Create the name of a table from a model name.
    - titleize: Capitalize all words and replace some characters for a nicer looking title.
    - transliterate: Replace non-ASCII characters with ASCII approximations.
    - underscore: Make an underscored, lowercase form from the expression in the string.

.. note::
    This module includes predefined rules for plural and singular forms, as well as a list of uncountable words.
"""

import re

import unicodedata

__all__ = [
    'camelize',
    'dasherize',
    'humanize',
    'ordinal',
    'ordinalize',
    'parameterize',
    'pluralize',
    'singularize',
    'tableize',
    'titleize',
    'transliterate',
    'underscore',
]

# ... (PLURALS, SINGULARS, and UNCOUNTABLES lists remain unchanged)
PLURALS = [
    (r"(?i)(quiz)$", r'\1zes'),
    (r"(?i)^(oxen)$", r'\1'),
    (r"(?i)^(ox)$", r'\1en'),
    (r"(?i)(m|l)ice$", r'\1ice'),
    (r"(?i)(m|l)ouse$", r'\1ice'),
    (r"(?i)(passer)s?by$", r'\1sby'),
    (r"(?i)(matr|vert|ind)(?:ix|ex)$", r'\1ices'),
    (r"(?i)(x|ch|ss|sh)$", r'\1es'),
    (r"(?i)([^aeiouy]|qu)y$", r'\1ies'),
    (r"(?i)(hive)$", r'\1s'),
    (r"(?i)([lr])f$", r'\1ves'),
    (r"(?i)([^f])fe$", r'\1ves'),
    (r"(?i)sis$", 'ses'),
    (r"(?i)([ti])a$", r'\1a'),
    (r"(?i)([ti])um$", r'\1a'),
    (r"(?i)(buffal|potat|tomat)o$", r'\1oes'),
    (r"(?i)(bu)s$", r'\1ses'),
    (r"(?i)(alias|status)$", r'\1es'),
    (r"(?i)(octop|vir)i$", r'\1i'),
    (r"(?i)(octop|vir)us$", r'\1i'),
    (r"(?i)^(ax|test)is$", r'\1es'),
    (r"(?i)s$", 's'),
    (r"$", 's'),
]

SINGULARS = [
    (r"(?i)(database)s$", r'\1'),
    (r"(?i)(quiz)zes$", r'\1'),
    (r"(?i)(matr)ices$", r'\1ix'),
    (r"(?i)(vert|ind)ices$", r'\1ex'),
    (r"(?i)(passer)sby$", r'\1by'),
    (r"(?i)^(ox)en", r'\1'),
    (r"(?i)(alias|status)(es)?$", r'\1'),
    (r"(?i)(octop|vir)(us|i)$", r'\1us'),
    (r"(?i)^(a)x[ie]s$", r'\1xis'),
    (r"(?i)(cris|test)(is|es)$", r'\1is'),
    (r"(?i)(shoe)s$", r'\1'),
    (r"(?i)(o)es$", r'\1'),
    (r"(?i)(bus)(es)?$", r'\1'),
    (r"(?i)(m|l)ice$", r'\1ouse'),
    (r"(?i)(x|ch|ss|sh)es$", r'\1'),
    (r"(?i)(m)ovies$", r'\1ovie'),
    (r"(?i)(s)eries$", r'\1eries'),
    (r"(?i)([^aeiouy]|qu)ies$", r'\1y'),
    (r"(?i)([lr])ves$", r'\1f'),
    (r"(?i)(tive)s$", r'\1'),
    (r"(?i)(hive)s$", r'\1'),
    (r"(?i)([^f])ves$", r'\1fe'),
    (r"(?i)(t)he(sis|ses)$", r"\1hesis"),
    (r"(?i)(s)ynop(sis|ses)$", r"\1ynopsis"),
    (r"(?i)(p)rogno(sis|ses)$", r"\1rognosis"),
    (r"(?i)(p)arenthe(sis|ses)$", r"\1arenthesis"),
    (r"(?i)(d)iagno(sis|ses)$", r"\1iagnosis"),
    (r"(?i)(b)a(sis|ses)$", r"\1asis"),
    (r"(?i)(a)naly(sis|ses)$", r"\1nalysis"),
    (r"(?i)([ti])a$", r'\1um'),
    (r"(?i)(n)ews$", r'\1ews'),
    (r"(?i)(ss)$", r'\1'),
    (r"(?i)s$", ''),
]

UNCOUNTABLES = {
    'equipment',
    'fish',
    'information',
    'jeans',
    'money',
    'rice',
    'series',
    'sheep',
    'species'
}


def _irregular(singular: str, plural: str, *plurals: str) -> None:
    """
    A convenience function to add appropriate rules to plurals and singular for irregular words.

    :param singular: irregular word in singular form (such as `it`)
    :type singular: str
    :param plural: irregular word in plural form (such as `they`)
    :type plural: str
    :param plurals: extended words in plural form (such as `them`)
    :type plurals: str

    This function adds case-insensitive rules for irregular word forms to the PLURALS and SINGULARS lists.
    It handles both capitalized and lowercase versions of the words.

    Example usage:
        _irregular('person', 'people')
        _irregular('child', 'children')
    """

    def caseinsensitive(string: str) -> str:
        return ''.join('[' + char + char.upper() + ']' for char in string)

    def _register_singular(singular_: str, plural_: str) -> None:
        if singular_[0].upper() == plural_[0].upper():
            SINGULARS.insert(0, (
                r"(?i)({}){}$".format(plural_[0], plural_[1:]),
                r'\1' + singular_[1:]
            ))
        else:
            SINGULARS.insert(0, (
                r"{}{}$".format(plural_[0].upper(), caseinsensitive(plural_[1:])),
                singular_[0].upper() + singular_[1:]
            ))
            SINGULARS.insert(0, (
                r"{}{}$".format(plural_[0].lower(), caseinsensitive(plural_[1:])),
                singular_[0].lower() + singular_[1:]
            ))

    def _register_plural(singular_: str, plural_: str) -> None:
        if singular_[0].upper() == plural_[0].upper():
            PLURALS.insert(0, (
                r"(?i)({}){}$".format(singular_[0], singular_[1:]),
                r'\1' + plural_[1:]
            ))
            PLURALS.insert(0, (
                r"(?i)({}){}$".format(plural_[0], plural_[1:]),
                r'\1' + plural_[1:]
            ))
        else:
            PLURALS.insert(0, (
                r"{}{}$".format(singular_[0].upper(),
                                caseinsensitive(singular_[1:])),
                plural_[0].upper() + plural_[1:]
            ))
            PLURALS.insert(0, (
                r"{}{}$".format(singular_[0].lower(),
                                caseinsensitive(singular_[1:])),
                plural_[0].lower() + plural_[1:]
            ))
            PLURALS.insert(0, (
                r"{}{}$".format(plural_[0].upper(), caseinsensitive(plural_[1:])),
                plural_[0].upper() + plural_[1:]
            ))
            PLURALS.insert(0, (
                r"{}{}$".format(plural_[0].lower(), caseinsensitive(plural_[1:])),
                plural_[0].lower() + plural_[1:]
            ))
        pass

    _register_plural(singular, plural)
    for p in [plural, *plurals]:
        _register_singular(singular, p)


def camelize(string: str, uppercase_first_letter: bool = True) -> str:
    """
    Convert strings to CamelCase.

    :param string: Original string to be converted
    :type string: str
    :param uppercase_first_letter: If True, converts to UpperCamelCase; if False, to lowerCamelCase
    :type uppercase_first_letter: bool
    :return: The camelized string
    :rtype: str

    This function converts strings to CamelCase. If `uppercase_first_letter` is True (default),
    it produces UpperCamelCase. If False, it produces lowerCamelCase.

    Examples:
        >>> camelize("device_type")
        'DeviceType'
        >>> camelize("device_type", False)
        'deviceType'

    Note:
        camelize can be thought of as a inverse of underscore, although there are some cases
        where that does not hold:
        >>> camelize(underscore("IOError"))
        'IoError'
    """
    if uppercase_first_letter:
        return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), string)
    else:
        return string[0].lower() + camelize(string)[1:]


def dasherize(word: str) -> str:
    """
    Replace underscores with dashes in the string.

    :param word: Original word to be dasherized
    :type word: str
    :return: The dasherized string
    :rtype: str

    This function replaces all underscores in the input string with dashes.

    Example:
        >>> dasherize("puni_puni")
        'puni-puni'
    """
    return word.replace('_', '-')


def humanize(word: str) -> str:
    """
    Capitalize the first word and turn underscores into spaces and strip a trailing "_id", if any.

    :param word: Original word to be humanized
    :type word: str
    :return: The humanized string
    :rtype: str

    This function is meant for creating pretty output. It capitalizes the first word,
    replaces underscores with spaces, and removes a trailing "_id" if present.

    Examples:
        >>> humanize("employee_salary")
        'Employee salary'
        >>> humanize("author_id")
        'Author'
    """
    word = re.sub(r"_id$", "", word)
    word = word.replace('_', ' ')
    word = re.sub(r"(?i)([a-z\d]*)", lambda m: m.group(1).lower(), word)
    word = re.sub(r"^\w", lambda m: m.group(0).upper(), word)
    return word


def ordinal(number: int) -> str:
    """
    Return the suffix that should be added to a number to denote the position in an ordered sequence.

    :param number: The number for which to generate the ordinal suffix
    :type number: int
    :return: The ordinal suffix (e.g., 'st', 'nd', 'rd', 'th')
    :rtype: str

    This function returns the appropriate suffix for ordinal numbers (1st, 2nd, 3rd, 4th, etc.).

    Examples:
        >>> ordinal(1)
        'st'
        >>> ordinal(2)
        'nd'
        >>> ordinal(1002)
        'nd'
        >>> ordinal(1003)
        'rd'
        >>> ordinal(-11)
        'th'
        >>> ordinal(-1021)
        'st'
    """
    number = abs(int(number))
    if number % 100 in (11, 12, 13):
        return "th"
    else:
        return {
            1: "st",
            2: "nd",
            3: "rd",
        }.get(number % 10, "th")


def ordinalize(number: int) -> str:
    """
    Turn a number into an ordinal string used to denote the position in an ordered sequence.

    :param number: The number to be ordinalized
    :type number: int
    :return: The ordinalized number as a string
    :rtype: str

    This function converts a number into its ordinal form (1st, 2nd, 3rd, 4th, etc.).

    Examples:
        >>> ordinalize(1)
        '1st'
        >>> ordinalize(2)
        '2nd'
        >>> ordinalize(1002)
        '1002nd'
        >>> ordinalize(1003)
        '1003rd'
        >>> ordinalize(-11)
        '-11th'
        >>> ordinalize(-1021)
        '-1021st'
    """
    return "{}{}".format(number, ordinal(number))


def parameterize(string: str, separator: str = '-') -> str:
    """
    Replace special characters in a string so that it may be used as part of a 'pretty' URL.

    :param string: Original string to be parameterized
    :type string: str
    :param separator: Separator to use between words (default is '-')
    :type separator: str
    :return: The parameterized string
    :rtype: str

    This function replaces special characters and spaces with the specified separator,
    making the string suitable for use in URLs.

    Example:
        >>> parameterize(u"Donald E. Knuth")
        'donald-e-knuth'
    """
    string = transliterate(string)
    # Turn unwanted chars into the separator
    string = re.sub(r"(?i)[^a-z0-9\-_]+", separator, string)
    if separator:
        re_sep = re.escape(separator)
        # No more than one of the separator in a row.
        string = re.sub(r'%s{2,}' % re_sep, separator, string)
        # Remove leading/trailing separator.
        string = re.sub(r"(?i)^{sep}|{sep}$".format(sep=re_sep), '', string)

    return string.lower()


def pluralize(word: str) -> str:
    """
    Return the plural form of a word.

    :param word: Original word to be pluralized
    :type word: str
    :return: The pluralized word
    :rtype: str

    This function returns the plural form of the given word based on predefined rules.

    Examples:
        >>> pluralize("posts")
        'posts'
        >>> pluralize("octopus")
        'octopi'
        >>> pluralize("sheep")
        'sheep'
        >>> pluralize("CamelOctopus")
        'CamelOctopi'
    """
    if not word or word.lower() in UNCOUNTABLES:
        return word
    else:
        for rule, replacement in PLURALS:
            if re.search(rule, word):
                return re.sub(rule, replacement, word)
        return word


def singularize(word: str) -> str:
    """
    Return the singular form of a word, the reverse of pluralize.

    :param word: Original word to be singularized
    :type word: str
    :return: The singularized word
    :rtype: str

    This function returns the singular form of the given word based on predefined rules.

    Examples:
        >>> singularize("posts")
        'post'
        >>> singularize("octopi")
        'octopus'
        >>> singularize("sheep")
        'sheep'
        >>> singularize("word")
        'word'
        >>> singularize("CamelOctopi")
        'CamelOctopus'
    """
    for inflection in UNCOUNTABLES:
        if re.search(r'(?i)\b(%s)\Z' % inflection, word):
            return word

    for rule, replacement in SINGULARS:
        if re.search(rule, word):
            return re.sub(rule, replacement, word)
    return word


def tableize(word: str) -> str:
    """
    Create the name of a table like Rails does for models to table names.

    :param word: Original word to be tableized
    :type word: str
    :return: The tableized word
    :rtype: str

    This method uses the pluralize method on the last word in the string after underscoring it.

    Examples:
        >>> tableize('RawScaledScorer')
        'raw_scaled_scorers'
        >>> tableize('egg_and_ham')
        'egg_and_hams'
        >>> tableize('fancyCategory')
        'fancy_categories'
    """
    return pluralize(underscore(word))


def titleize(word: str) -> str:
    """
    Capitalize all the words and replace some characters in the string to create a nicer looking title.

    :param word: Original word to be titleized
    :type word: str
    :return: The titleized string
    :rtype: str

    This function is meant for creating pretty output by capitalizing all words and
    replacing certain characters for improved readability.

    Examples:
      >>> titleize("man from the boondocks")
      'Man From The Boondocks'
      >>> titleize("x-men: the last stand")
      'X Men: The Last Stand'
      >>> titleize("TheManWithoutAPast")
      'The Man Without A Past'
      >>> titleize("raiders_of_the_lost_ark")
      'Raiders Of The Lost Ark'
    """
    return re.sub(
        r"\b('?\w)",
        lambda match: match.group(1).capitalize(),
        humanize(underscore(word)).title()
    )


def transliterate(string: str) -> str:
    """
    Replace non-ASCII characters with an ASCII approximation.

    :param string: Original string to be transliterated
    :type string: str
    :return: The transliterated string
    :rtype: str

    If no approximation exists, the non-ASCII character is ignored.
    The input string must be unicode.

    Examples:
        >>> transliterate('älämölö')
        'alamolo'
        >>> transliterate('Ærøskøbing')
        'rskbing'
    """
    normalized = unicodedata.normalize('NFKD', string)
    return normalized.encode('ascii', 'ignore').decode('ascii')


def underscore(word: str) -> str:
    """
    Make an underscored, lowercase form from the expression in the string.

    :param word: Original word to be underscored
    :type word: str
    :return: The underscored string
    :rtype: str

    This function converts CamelCase or space-separated words to lowercase, underscore-separated words.

    Example:
        >>> underscore("DeviceType")
        'device_type'

    Note:
        As a rule of thumb, you can think of underscore as the inverse of camelize,
        though there are cases where that does not hold:
            >>> camelize(underscore("IOError"))
            'IoError'
    """
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


# Irregular word definitions
_irregular('person', 'people')
_irregular('man', 'men')
_irregular('human', 'humans')
_irregular('child', 'children')
_irregular('sex', 'sexes')
_irregular('move', 'moves')
_irregular('cow', 'kine')
_irregular('zombie', 'zombies')

# Self added patterns
_irregular('it', 'they', 'them')
_irregular('this', 'these')
_irregular('that', 'those')
