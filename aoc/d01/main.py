import math
from typing import IO
import numpy as np


# this is the target number
FINAL_NUM = 2020

def binary_search(num_list, target):
    '''binary search for target thru num_list'''
    # assume the num_list is sorted here
    if len(num_list) == 1 and num_list[0] != target:
        return False

    mid_index = math.ceil(len(num_list)/2)
    mid = num_list[mid_index]

    #the below seems not great but it's what pylint wanted
    if mid == target:
        return True

    if mid < target:
        return binary_search(num_list[mid_index:], target)
    return binary_search(num_list[:mid_index], target)


def find_nums(numbers, target):
    '''find 2 numbers in the list of numbers that sums to target'''
    # assume numbers is a sorted num_list.

    # if it's just 2 numbers, i can split into numbers less than
    # target/2 and numbers greater than target/2. the numbers
    # i'm looking for, one will be in the first one will be in
    # the second

    for index, num in enumerate(numbers):
        if num < target/2:
            split_pt = index
        # need some sort of throw thing here

    list_1 = numbers[:split_pt]
    list_2 = numbers[split_pt:]

    # now i'm going to start with the smaller num_list (since that)
    # would be order n and search for the pair in the larger num_list
    # since that would be order log2n.
    if len(list_1) < len(list_2):
        main_list = list_1
        search_list = list_2
    else:
        main_list = list_2
        search_list = list_1

    # now go thru mainlist and search for the pair in the search num_list
    for x_1 in main_list:
        x_2 = target-x_1
        if binary_search(search_list, x_2):
            return [x_1, x_2]

    return []


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    ''' read the file in as a num_list of nums then return the product of 2 numbers
    in the list that sum to the final value'''
    numbers = [int(line.rstrip('\n')) for line in input_file]
    numbers.sort()
    product = np.prod(find_nums(numbers, FINAL_NUM))

    if product > 0:
        output = product
    else:
        output = 0
    return output

def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''find 3 numbers that sum to  the final_num and return their product'''
    # read the file in as a num_list of nums
    numbers = [int(line.rstrip('\n')) for line in input_file]

    # sort the num_list
    numbers.sort()

    # what we're going to do is start with the first, then
    # run the first main find nums p_1 algorithm on the difference btw
    # 2020 and the first number.
    # the first algo is o(nlogn), this will be o(n^2logn)
    for k, x_1 in enumerate(numbers):
        target = FINAL_NUM - x_1
        result = find_nums(numbers[k+1:], target)
        if result:
            return np.prod(result)*x_1
    return None
