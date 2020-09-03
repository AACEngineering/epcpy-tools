import re

GTIN_MATCH = re.compile(r'^\d{8}$|^\d{12,14}$')


def calc_check_digit(upc_string):
    odd_sum = 0
    even_sum = 0

    for i, char in enumerate(upc_string):
        if (i + 1) % 2 == 0:
            even_sum += int(char)
        else:
            odd_sum += int(char) * 3

    return 10 - ((odd_sum + even_sum) % 10)


def is_valid_upc(upc_string):
    match = GTIN_MATCH.match(upc_string)

    if not match:
        return False

    return calc_check_digit(upc_string[:-1]) == int(upc_string[-1])
