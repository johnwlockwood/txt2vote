from functools import partial
from itertools import imap
import string

# Higher order
from standardize_address import expand_standardize_abbr
from standardize_address import lookup_standardize_abbr
from standardize_address import title_case_string


def lower_getter(getter, data):
    """
    Lower cases the result of the getter given data.
    """
    return string.lower(str(getter(data)))


def lower_list_getter(getter, data):
    """
    Lower cases the items in the result of the getter given data.
    """
    value = getter(data)
    if isinstance(value, tuple):
        return map(string.lower, map(str, value))
    return string.lower(str(value))


def title_getter(getter, data):
    """
    Title cases the result of the getter given data.
    """
    return title_case_string(str(getter(data)))


def title_list_getter(getter, data):
    """
    Title cases the items in the result of the getter given data.
    """
    return map(title_case_string, map(str, getter(data)))


def number_getter(getter, data):
    """
    Gets the leading digits from the result of the getter given data.
    """
    return get_number_prefix(getter(data))


def join_stripped_gotten_value(sep, getters, data):
    """
    Join the values, coerced to str and stripped of whitespace padding,
    from entity, gotten with collection of getters,
    with the separator.

    :param sep: :class: `str` Separator of values.
    :param getters: collection of callables takes that data and returns value.
    :param data: argument for the getters
    """
    return sep.join(
        filter(
            None,
            imap(string.strip,
                 imap(str,
                      filter(None, [getter(data) for getter in getters])))))


def join_stripped_values(sep, collection_getter, data):
    """
    Join the values, coerced to str and stripped of whitespace padding,
    from entity, gotten with collection_getter,
    with the separator.

    :param sep: :class: `str` Separator of values.
    :param collection_getter: callable takes that data and returns collection.
    :param data: argument for the collection_getter
    """
    value = collection_getter(data)
    if not isinstance(value, tuple):
        value = (value,)
    return sep.join(
        filter(
            None,
            imap(string.strip,
                 imap(str, filter(None, value)))))


# High order

def get_full_name(name_parts_getter, data):
    """
    Space join the non-empty values from data with the name parts getter.
    """
    return join_stripped_values(' ', name_parts_getter, data)


def get_phone(phone_parts_getter, data):
    """
    Dash join the non-empty values from data with the phone parts getter.

    The phone_parts_getter should return
    the area code, exchange and last four.
    """
    return join_stripped_values('-', phone_parts_getter, data)


def get_zip(zip_parts_getter, data):
    """
    Dash join non-empty values from data with the zip parts getter.
    """
    return join_stripped_values('-', zip_parts_getter, data)


# Addresses
def get_number_prefix(number):
    number = str(number)

    if not number:
        return ""
    try:
        number = str(int(number))
    except (ValueError, TypeError), e:
        digits = []
        for digit in number:
            if digit in string.digits:
                digits.append(digit)
            else:
                break
        number = "".join(digits)
    return number


def get_raw_address_label(address_parts_getter, data):
    """
    Get the address label for use with in the geocoder.
    Space join non-empty parts of the address label
    from the data.

    """

    return join_stripped_values(' ', address_parts_getter, data)


def get_geocodable_address_label(house_number_getter,
                                 street_name_getter,
                                 data):
    """
    Get the address label for use with the geocoder
    using separate getters. Space join non-empty parts
    """
    value = title_case_string(
        expand_standardize_abbr(join_stripped_gotten_value(
            ' ', (house_number_getter,
                  street_name_getter), data)))
    if "'" in value:
        return value.replace("'", "")
    return value


def get_address_label(address_parts_getter, data):
    return lookup_standardize_abbr(
        get_raw_address_label(address_parts_getter, data))


def get_address(address_label_getter,
                city_getter,
                state_getter,
                zip_parts_getter,
                data):
    """
    Get the address for use in the geocoder.
    Comma-space join non-empty parts of the address
    from the data.

    """
    return [join_stripped_gotten_value(
        ', ', (
            address_label_getter,
            city_getter,
            state_getter,
            partial(get_zip, zip_parts_getter)
        ),
        data)]


def get_separated_address(address_label_getter,
                          city_getter,
                          state_getter,
                          zip_parts_getter,
                          data):
    """
    Get the address for use in the geocoder.
    Comma-space join non-empty parts of the address
    from the data.

    """
    return (address_label_getter(data),
            city_getter(data),
            state_getter(data),
            get_zip(zip_parts_getter, data))

# get_geocoder_address just passes in the get_raw_address_label
# get_full_address passes in address label
# getter that runs lookup_standardize_abbr on the value.


def get_unit(unit_parts_getter, data):
    return join_stripped_values(' ', unit_parts_getter, data)


def get_zip_road(zip5_getter, road_getter, data):
    return join_stripped_gotten_value('|', (zip5_getter, road_getter), data)

