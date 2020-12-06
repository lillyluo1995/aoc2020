from typing import IO
import math


def calc_num(code, low, high):
    '''given a binary seat code and a total number of seats, calc
    the correct seat for this'''

    # check that it corresponds....need to add 1 bc 0 index
    assert math.pow(2, len(code)) == (high-low+1)

    if len(code) == 1:
        if code in ['B', 'R']:
            return high
        return low
    if code[0] in ['B', 'R']:
        return calc_num(code[1:], low+(high-low+1)/2, high)
    return calc_num(code[1:], low, high-(high-low+1)/2)


def calc_seat_id(code, num_rows, num_cols):
    '''given the string code, calculate what the seat id is '''
    row_code = code[0:int(math.log2(num_rows))]
    col_code = code[-int(math.log2(num_cols)):]

    row_num = calc_num(row_code, 0, num_rows-1)
    col_num = calc_num(col_code, 0, num_cols-1)

    return row_num*8+col_num


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''find the highest seat id in the given list of seats'''
    codes = [line.rstrip('\n') for line in input_file]

    # sort the codes. B = higher so ok to sort by ascending since B < F
    # we multiply the first number by 8 so the impact of the first 7 chars
    # will be larger than any impact the last 3 can have
    codes.sort()

    return calc_seat_id(codes[0], 128, 8)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''now find my seat. the flight is full except front/back'''
    num_rows = 128
    num_cols = 8

    codes = [line.rstrip('\n') for line in input_file]
    codes.sort()
    # ok now i need to find my seat. it's not hte first or last row....
    # so first i need to find the code that denotes the first row
    # and then find the code that denotes the last row
    max_row = calc_num(codes[0][0:int(math.log2(num_rows))], 0, num_rows-1)
    min_row = calc_num(codes[-1][0:int(math.log2(num_rows))], 0, num_rows-1)

    # the lower bound for my seat is the last seat in the first row
    # and the upper bound for my seat is the first seat in the last row
    min_seat = int(max([min_row*8+i for i in range(7)]))
    max_seat = int(min([max_row*8+i for i in range(7)]))

    seat_codes = {calc_seat_id(x, num_rows, num_cols) for x in codes}
    all_seats = set(range(min_seat, max_seat))

    return all_seats - seat_codes
