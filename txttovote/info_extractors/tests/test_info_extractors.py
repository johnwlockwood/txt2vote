from operator import itemgetter

import unittest

from karld.conversion_operators import join_stripped_values
from karld.conversion_operators import join_stripped_gotten_value

from info_extractors import get_full_name
from info_extractors import get_phone
from info_extractors import get_zip
from info_extractors import number_getter
from info_extractors import lower_getter
from info_extractors import lower_list_getter
from info_extractors import title_getter
from info_extractors import title_list_getter
from info_extractors import get_number_prefix


class TestValueJoiner(unittest.TestCase):
    def test_join_stripped_values(self):
        """
        Ensure joiner gets the values from
        data with the getter, coerce to str,
        strips padding whitespace and join
        with the separator.
        """
        getter = itemgetter(0, 1, 2, 3)
        data = (" A", "B ", 2, "D")
        separator = "+"
        self.assertEqual(join_stripped_values(separator, getter, data),
                         "A+B+2+D")


class TestGettersValueJoiner(unittest.TestCase):
    def test_join_stripped_gotten_value(self):
        """
        Ensure joiner gets the values from
        data with the getters, coerce to str,
        strips padding whitespace and join
        with the separator.
        """
        getters = (itemgetter(0), itemgetter(1), itemgetter(2), itemgetter(3))
        data = (" A", "B ", 2, "D")
        separator = "+"
        self.assertEqual(join_stripped_gotten_value(separator, getters, data),
                         "A+B+2+D")


class TestFullName(unittest.TestCase):
    def test_full_name_builds_full_name(self):
        """
        Ensure name parts of the data are extracted
        and joined with a space, excluding empty parts,
        and stripping padding spaces.
        """
        data = [
            ("Jack ", "12356", "Danger", "Johnson"),
            (" Mary", "54354", "", "Hill"),
        ]

        name_parts_getter = itemgetter(0, 2, 3)

        self.assertEqual(get_full_name(name_parts_getter, data[0]),
                         "Jack Danger Johnson")

        self.assertEqual(get_full_name(name_parts_getter, data[1]),
                         "Mary Hill")


class TestPhone(unittest.TestCase):
    def test_get_phone_builds_phone(self):
        """
        Ensure phone parts of the data are extracted
        and joined with a space, excluding empty parts,
        and stripping padding spaces.
        """
        data = [
            ("Jack ", "3801", "479", 981, "Johnson"),
            (" Mary", "1234", "555", "155", "Hill"),
            ("Bob", "2234", "", "155", "Ted"),
        ]

        phone_parts_getter = itemgetter(2, 3, 1)

        self.assertEqual(get_phone(phone_parts_getter, data[0]),
                         "479-981-3801")

        self.assertEqual(get_phone(phone_parts_getter, data[1]),
                         "555-155-1234")

        self.assertEqual(get_phone(phone_parts_getter, data[2]),
                         "155-2234")

    def test_get_zip(self):
        """
        Ensure get_zip calls uses - for the separator and
        gets all the benefits of join_stripped_values.
        """
        self.assertEqual(get_zip(itemgetter(0, 1), (" 2", 3)), "2-3")


class TestGetterTransformers(unittest.TestCase):
    def test_get_number_prefix_none(self):
        """
        Ensure get_number_prefix returns an empty
        string given None
        """
        self.assertEqual("", get_number_prefix(None))

    def test_get_number_prefix_number(self):
        """
        Ensure get_number_prefix returns the same
        string when it is given one with all digits
        """
        self.assertEqual("1234", get_number_prefix("1234"))

    def test_get_number_prefix_float(self):
        """
        Ensure get_number_prefix returns the
        first digits when it is given a float
        """
        self.assertEqual("123", get_number_prefix("123.99"))

    def test_get_number_prefix_letter(self):
        """
        Ensure get_number_prefix returns the
        first digits when it is given a float
        """
        self.assertEqual("99", get_number_prefix("99b"))

    def test_get_number_prefix_only(self):
        """
        Ensure get_number_prefix returns the
        first digits when it is given a float
        """
        self.assertEqual("", get_number_prefix("b99"))

    def test_number_getter(self):
        """
        Ensure number_getter takes only the first digits
        of a string.
        """
        data = ("123b",)
        getter = itemgetter(0)
        self.assertEqual("123", number_getter(getter, data))

    def test_lower_getter(self):
        """
        Ensure lower_getter returns the lower case of
        the results of the getter given data.
        """
        data = ("HELLO WOrld",)
        getter = itemgetter(0)
        self.assertEqual("hello world", lower_getter(getter, data))

    def test_lower_list_getter(self):
        """
        Ensure lower_getter returns the lower case of
        the results of the getter given data.
        """
        data = ("HELLO", "WOrld",)
        getter = itemgetter(0, 1)
        self.assertEqual(["hello", "world"],
                         lower_list_getter(getter, data))

    def test_title_getter(self):
        """
        Ensure title_getter returns the lower case of
        the results of the getter given data.
        """
        data = ("HELLO WOrld",)
        getter = itemgetter(0)
        self.assertEqual("Hello World", title_getter(getter, data))

    def test_title_list_getter(self):
        """
        Ensure title_getter returns the lower case of
        the results of the getter given data.
        """
        data = ("HELLO", "WOrld",)
        getter = itemgetter(0, 1)
        self.assertEqual(["Hello", "World"],
                         title_list_getter(getter, data))


