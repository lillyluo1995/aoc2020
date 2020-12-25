from typing import IO
import re
import itertools

from aoc.common import helpers


def process_file_1(input_file):
    '''process the chunks of file. only need numbers here'''
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


def process_file_2(input_file):
    '''process the chunks of file. need more info here too'''
    chunk = 0
    pair_ranges = {}
    other_tickets = []
    for line in input_file.readlines():
        if line == '\n':
            chunk += 1
            continue
        if chunk == 0:  # this is the specification side
            ticket_section, specs = re.split(r":\s", line)
            num_ranges = [int(num) for num in re.findall('[0-9]+', specs)]
            pairs = [(num_ranges[i], num_ranges[i+1])
                     for i in range(0, len(num_ranges), 2)]
            pair_ranges[ticket_section] = pairs
        if chunk == 1:  # this is my ticket
            nums = [int(num) for num in re.findall('[0-9]+', line)]
            if len(nums) == 0:
                continue
            my_ticket = nums
        elif chunk == 2:  # the other tickets
            nums = [int(num) for num in re.findall('[0-9]+', line)]
            if len(nums) == 0:
                continue
            other_tickets.append(nums)
    return pair_ranges, my_ticket, other_tickets


def find_bad_tickets(pairs, tickets):
    '''given a list of tickets, return the bad values and the indices \
        of the bad tickets'''
    # sort both
    pairs.sort()
    tickets.sort()

    bad_nums = []
    bad_tix = set()
    # i guess i'll just do it naively first...

    for idx, ticket in enumerate(tickets):
        for num in ticket:
            good = False
            for pair in pairs:
                if pair[0] <= num <= pair[1]:
                    good = True
            if not good:
                bad_nums.append(num)
                bad_tix.add(idx)
    return bad_nums, bad_tix

def get_possible_mapping(ranges, tickets):
    '''given ranges of acceptable numbers and a set of tickets, return
    a mapping of seat label --> possible idx'''
    mapping = {}
    for label, range_ in ranges.items():
        for idx in range(len(tickets[0])):
            correct_label = True
            for ticket in tickets:
                if not (range_[0][0] <= ticket[idx] <= range_[0][1]
                        or range_[1][0] <= ticket[idx] <= range_[1][1]):
                    correct_label = False
            if correct_label:
                if label in mapping:
                    mapping[label].append(idx)
                else:
                    mapping[label] = [idx]
    return mapping

def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''sum the nearby tix that don't fit any of the criteria'''
    num_ranges, _, nearby_tickets = process_file_1(input_file)
    pairs = [(num_ranges[i], num_ranges[i+1])
             for i in range(0, len(num_ranges), 2)]
    bad_nums, _ = find_bad_tickets(pairs, nearby_tickets)
    return sum(bad_nums)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''part 2'''
    num_ranges, my_ticket, nearby_tickets = process_file_2(input_file)
    pairs_list = list(itertools.chain(*list(num_ranges.values())))
    _, bad_tix = find_bad_tickets(pairs_list, nearby_tickets)

    # below are the good tickets
    good_tix = [ticket for idx, ticket in enumerate(nearby_tickets)
                if idx not in bad_tix]

    mapping = get_possible_mapping(num_ranges, good_tix)
    final_mapping = helpers.organize_idx_map(mapping)

    req_prod = 1
    for idx, num in enumerate(my_ticket):
        if 'departure' in final_mapping[idx]:
            req_prod *= num
    return req_prod
