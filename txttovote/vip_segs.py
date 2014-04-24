__doc__ = """
start_house_number
end_house_number
odd_even_both
start_apartment_number
end_apartment_number
non_house_address_address_direction
non_house_address_street_name
non_house_address_house_number_prefix
non_house_address_city
non_house_address_street_suffix
non_house_address_state
non_house_address_street_direction
non_house_address_house_number_suffix
non_house_address_zip
non_house_address_apartment
non_house_address_house_number
precinct_id
precinct_split_id
id
"""

from functools import partial
from itertools import chain
from operator import itemgetter
import argparse
from datetime import datetime

from karld.run_together import pool_run_files_to_files
from karld.run_together import csv_file_to_file

from data_pipelines.to_geocode import to_geocode_addresses

from info_extractors import get_separated_address, join_stripped_gotten_value
from info_extractors import get_geocodable_address_label
from info_extractors import title_getter
from info_extractors import number_getter

def get_street(data):
    return join_stripped_gotten_value(
            ' ', (itemgetter(6),
                  itemgetter(9)), data)

def named_getters():
    return {
        'id': itemgetter(-1),
        "gc_house_number": partial(number_getter, itemgetter(0)),
        "street_name": partial(title_getter, itemgetter(6)),
        "city_getter": partial(title_getter, itemgetter(8)),
        "state_getter": itemgetter(10),
        "zip_parts_getter": itemgetter(13),
        "address_combiner": get_separated_address,
        "geocode_header": ("id", "Address", "City", "State", "Zip"),
        "gc_address_label_getter": partial(get_geocodable_address_label,
                                           itemgetter(0), get_street)
    }


def run_test_geocode():
    csv_file_to_file(
        partial(to_geocode_addresses, named_getters),
        "to_geocode_",
        "../vipdata/ma/seg_out_to_gc/",
        ("../vipdata/outdc/street_segment.txt",
         "street_segment.txt"))


def run_together_geocode():
    pool_run_files_to_files(
        partial(csv_file_to_file,
                partial(to_geocode_addresses, named_getters),
                "to_geocode_",
                "../vipdata/ma/seg_out_to_gc/"),
        "../vipdata/outdc/street_segments")


def main(*args):
    parser = argparse.ArgumentParser(*args)
    parser.add_argument("mode",
                        help="Run mode")
    args = parser.parse_args()

    if args.mode == "to-geocode":
        run_together_geocode()
    elif args.mode == "test-g":
        run_test_geocode()


if __name__ == "__main__":
    main()
