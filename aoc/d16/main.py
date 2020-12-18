from typing import IO
import re


def process_file(input_file):
    '''process the chunks of file'''
    sets = []
    complete_set = []
    for line in input_file.readlines():
        numbers = re.findall('[0-9]+', line)
        if len(numbers) == 0:  # if i get an empty row
            if len(sets) > 1:  # bc len([[]]) = 1....
                complete_set.append(sets)
                sets = []
        else:
            numbers = [int(num) for num in numbers]
            sets = sets + numbers
    return complete_set + [sets]  # this is the last one. must be cleaner way


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''sum the nearby tix that don't fit any of the criteria'''
    num_ranges, _, nearby_tickets = process_file(input_file)
    pairs = [(num_ranges[i], num_ranges[i+1])
             for i in range(0, len(num_ranges), 2)]

    # sort both
    pairs.sort()
    nearby_tickets.sort()

    bad_nums_sum = 0

    # i guess i'll just do it naively first...
    for num in nearby_tickets:
        good = False
        for pair in pairs:
            if pair[0] <= num <= pair[1]:
                good = True
        if not good:
            bad_nums_sum += num

    return bad_nums_sum


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''part 2'''
    return input_file
