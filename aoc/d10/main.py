from typing import IO
from collections import deque
from functools import lru_cache


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

def find_iteration_wrapper(adaptors, target):
    '''wrapper to take in the adaptors argument'''
    @lru_cache()
    def find_iteration(target):
        '''how many ways are there to reach target?'''
        if len(adaptors) == 0:
            return 0
        if target == 0:
            return 1
        if target == 1:
            return 1

        possible = {target-i for i in range(1, 4)}

        #this can be optimized if necessary to not pass in all of adaptors
        #but it didn't seem like it had a huge impact on run time vs the cache...
        #n isn't that high after all
        existing = [x for x in adaptors if x in possible and x >= 0]
        total_iterations = sum([find_iteration(x)
                                for x in existing])
        return total_iterations

    return find_iteration(target)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''how many ways are there to arrange the adaptors
    so that the max is still reached'''
    adaptors = [0] + parse_file(input_file)

    # first sort the adaptors
    adaptors.sort()

    #since sorted by ascending target is the last element
    return find_iteration_wrapper(adaptors, adaptors[-1])
