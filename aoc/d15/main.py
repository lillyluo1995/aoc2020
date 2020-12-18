from typing import IO
import re


def read_file(input_file):
    '''read file and return the starting numbers'''
    starting_numbers = re.split(',', input_file.readlines()[0])
    return [int(num) for num in starting_numbers]


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''given the first 3 starting numbers and set of rules, what is the 2020 number'''
    numbers = read_file(input_file)
    target = 2020
    counter = len(numbers)
    num_idx_map = {num: idx for idx, num in enumerate(numbers)}
    while counter < target:
        most_recent = numbers[-1]
        if most_recent not in num_idx_map:
            numbers.append(0)
            num_idx_map[most_recent] = counter-1
        else:
            numbers.append(counter-1-num_idx_map[most_recent])
            num_idx_map[most_recent] = counter-1
        counter += 1
    return numbers[-1]


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''there needs to be a faster way to do this. this version took a while'''
    numbers = read_file(input_file)
    target = 30000000
    counter = len(numbers)
    num_idx_map = {num: idx for idx, num in enumerate(numbers)}
    while counter < target:
        most_recent = numbers[-1]
        if most_recent not in num_idx_map:
            numbers.append(0)
            num_idx_map[most_recent] = counter-1
        else:
            numbers.append(counter-1-num_idx_map[most_recent])
            num_idx_map[most_recent] = counter-1
        counter += 1
    return numbers[-1]
