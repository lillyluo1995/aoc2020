from typing import IO
from collections import deque


def parse_file(input_file):
    '''read the input file into a list of ints'''
    return [int(x) for x in input_file.readlines()]


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''what is number of 1 diffs * number of 3 diffs'''
    # add 0 for the initial one
    adaptors = [0] + parse_file(input_file)

    # first we need to sort them
    adaptors.sort()

    # now put adaptors into a queue so we can pop out more easily (we
    # just care about the order, we don't need things to stay there)
    adaptors = deque(adaptors)

    # now we just loop thru and find the number that are diff by 1
    # and the number that are diff by three
    num_1 = 0
    num_3 = 0
    most_recent = 0
    while adaptors:
        head = adaptors.popleft()
        if head == 0:
            continue
        if head - most_recent == 1:
            num_1 += 1
            most_recent = head
        elif head - most_recent == 3:
            num_3 += 1
            most_recent = head
        else:
            print('error')

    # add 1 to num_3 because of the final adaptor
    return num_1 * (num_3+1)

#this global map really needs to be improved
BIG_MAP = {0: 1, 1: 1}


def find_num_iteration(adaptors):
    '''given a list of adaptors (assumed ascending sorted), return
    number of ways to get to the max in the list (which is the last one)'''
    if len(adaptors) == 0:
        return 0
    target = adaptors[-1]
    if target in BIG_MAP:
        return BIG_MAP[target]
    possible = {target-i for i in range(1, 4)}

    existing = []
    existing_idx = []
    if len(adaptors) <= 3:
        for idx, adaptor in enumerate(adaptors):
            adaptor = adaptors[idx]
            if adaptor in possible and adaptor >= 0:
                existing.append(adaptor)
                existing_idx.append(idx)
    else:
        for idx, adaptor in enumerate(adaptors[-4:]):
            if adaptor in possible and adaptor >= 0:
                existing.append(adaptor)
                existing_idx.append(idx-4)

    total_iterations = sum([find_num_iteration(adaptors[:x+1])
                            for x in existing_idx])
    BIG_MAP[target] = total_iterations
    return total_iterations


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''how many ways are there to arrange the adaptors
    so that the max is still reached'''
    adaptors = [0] + parse_file(input_file)

    # first sort the adaptors
    adaptors.sort()

    return find_num_iteration(adaptors)
