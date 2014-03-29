from datetime import datetime
from functools import partial
from itertools import chain
from operator import itemgetter

from info_extractors import get_address
from info_extractors import get_geocodable_address_label
from karld.conversion_operators import join_stripped_values
from standardize_address import title_case_string


def to_geocode_addresses(named_getters, data_items):
    """
    With the named getters extract the addresses
    into a form usable with a geo-coder.
    """
    getters = named_getters()
    label_getter = getters["gc_address_label_getter"]
    get_full_address_for_geocode = partial(
        getters.get("address_combiner", get_address),
        label_getter,
        getters["city_getter"],
        getters["state_getter"],
        getters["zip_parts_getter"]
    )
    get_id = getters["id"]

    results = (list(chain((get_id(item),),
                          get_full_address_for_geocode(item)))
               for item in data_items)
    header = getters.get("geocode_header")
    if header:
        results = chain((header,), results)

    return results


def len_of_from_getter(getter, item):
    value = getter(item)
    if not value:
        return 0
    return len(value)


def divide_getter(divide_by, getter, item):
    value = getter(item)
    if not value:
            return 0
    return value/divide_by
