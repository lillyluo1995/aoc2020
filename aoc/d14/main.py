from typing import IO
import re
import numpy as np


def apply_mask_1(bitmask, value):
    '''apply the bitmask to a binary value'''
    value_list = list(value)
    for idx, bit in enumerate(bitmask):
        if bit == 'X':
            continue
        value_list[idx] = bit
    return ''.join(value_list)


def apply_float_values(value_list):
    '''replace all the xs in value list with 0 or 1....recursively'''
    try:
        value_list = list(value_list)
        x_idx = value_list.index('X')
        value_list_1 = value_list[:]
        value_list_2 = value_list[:]
        value_list_1[x_idx] = '0'
        value_list_2[x_idx] = '1'

        return np.array([
            apply_float_values(value_list_1),
            apply_float_values(value_list_2)
        ])
    except ValueError:  # no more X, we are done!
        return ''.join(value_list)


def apply_mask_2(bitmask, value):
    '''apply the bitmask to a binary value....return an array'''
    value_list = list(value)
    for idx, bit in enumerate(bitmask):
        if bit == '0':
            continue
        if bit == '1':
            value_list[idx] = '1'
        elif bit == 'X':
            value_list[idx] = 'X'
    # now we have the value list updated....we need to consider all the
    # diff values that X can float to.
    value_lists = np.ndarray.flatten(apply_float_values(value_list))
    return [''.join(value_list) for value_list in value_lists]


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''apply the bitmasks and sum the values'''
    storage = [0]*75000
    for line in input_file.readlines():
        groups = re.split('[ =]+', line)
        if groups[0] == 'mask':
            bitmask = groups[1].replace('\n', '')
        else:  # this is a mem allocation
            _, idx, _ = re.split(r"[\[\]]+", groups[0])
            value = groups[1].replace('\n', '')
            value_bi = format(int(value), 'b')
            num_zeros_padding = 36 - len(value_bi)
            value_bi = '0'*num_zeros_padding + value_bi
            value = int(apply_mask_1(bitmask, value_bi), 2)
            storage[int(idx)] = value
    return sum(storage)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''use the different encoder'''
    storage = {}
    for line in input_file.readlines():
        groups = re.split('[ =]+', line)
        if groups[0] == 'mask':
            bitmask = groups[1].replace('\n', '')
        else:
            _, idx, _ = re.split(r"[\[\]]+", groups[0])
            value = groups[1].replace('\n', '')
            idx_bi = format(int(idx), 'b')
            num_zeros_padding = 36 - len(idx_bi)
            idx_bi = '0'*num_zeros_padding + idx_bi
            final_idxs = [int(x, 2) for x in apply_mask_2(bitmask, idx_bi)]
            for final_idx in final_idxs:
                storage[final_idx] = int(value)
    return sum(storage.values())
