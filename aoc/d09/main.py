from typing import IO


def check_num_sum(num_list, target):
    '''check whether there are two numbers in the list num_list that sum to target'''
    # first need to sort the list
    num_list.sort()  # o(logn)
    summed = False
    left = 0
    right = len(num_list)-1
    while not summed and left < right:
        total = num_list[left] + num_list[right]
        if total == target:
            summed = True
        elif total < target:
            left += 1
        else:
            right -= 1
    return summed


def return_first_num(num_list, preamble_length):
    '''return the first number where no numbers in the preceding list of
    preamble_length will not sum to it'''
    prop = True
    start = 0
    end = start + preamble_length
    while prop:
        sub_list = num_list[start:end]
        target = num_list[end]
        if not check_num_sum(sub_list, target):
            prop = False
            break
        start += 1
        end = start + preamble_length
    return target


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''for a given preamble length, return the first number that
    doesn't satisfy the preamble addition situation'''
    num_list = [int(line) for line in input_file.readlines()]
    return return_first_num(num_list, 25)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''return the sum of the smallest and largest numbers in a contiguous range
    that sum to the output in p_1'''

    num_list = [int(line) for line in input_file.readlines()]
    # this probably isn't the best....will
    target = return_first_num(num_list, 25)

    # 1. get the indices of all the numbers that are greater than target....
    bad_idx = [0] + \
        [idx for idx in range(len(num_list)) if num_list[idx] > target]
    # 2. we are going to create lists btw each of the idx start and end points...
    # since if a number is greater than the target, obvi we can't add up to it.
    for i, idx in enumerate(bad_idx):
        if i == len(bad_idx)-1:
            return ValueError
        idx_list = range(idx, bad_idx[i+1])
        for left in idx_list:
            for right in range(left, bad_idx[i+1]):
                test_list = num_list[left:right+1]
                if sum(test_list) == target:
                    return max(test_list)+min(test_list)
    return ValueError
