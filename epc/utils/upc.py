import re

GTIN_MATCH = re.compile(r'^\d{8}$|^\d{12,14}$')


def calc_check_digit(upc_string):
    evens = []
    odds = []

    for i, char in enumerate(upc_string):
        if (i + 2) % 2 == 0:
            evens.append(int(char))
        else:
            odds.append(int(char))

    return (10 - (((3 * sum(evens)) + sum(odds)) % 10)) % 10


def is_valid_upc(upc_string):
    match = GTIN_MATCH.match(upc_string)

    if not match:
        return False

    return calc_check_digit(upc_string[:-1]) == int(upc_string[-1])
