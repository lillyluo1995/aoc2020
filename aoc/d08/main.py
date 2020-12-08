from typing import IO
import re
import copy


def parse_instruction(inst):
    '''given inst which is a list of instructions, return the next index
    and what i should add to the accumulator'''
    dir_, incr = inst[0], int(inst[1])
    acc_incr = 0
    step_incr = 0
    if dir_ == 'acc':
        acc_incr = incr
        step_incr = 1
    elif dir_ == 'nop':
        acc_incr = 0
        step_incr = 1
    elif dir_ == 'jmp':
        acc_incr = 0
        step_incr = incr
    else:
        acc_incr = ValueError
        step_incr = ValueError
    return acc_incr, step_incr


def run_iteration(rules):
    '''run through the rules as intended, returns the final accum
    and whether or not it got thru all the rules'''
    # matches index of rules, tells me how many times i've been to one spot
    rules_ct = [0]*len(rules)

    # initialize accumulator value
    accum = 0

    not_repeated = True
    current_index = 0
    rules_ct[0] = 1
    finish = False
    while not_repeated:
        acc_incr, step_incr = parse_instruction(rules[current_index])
        current_index += step_incr
        accum += acc_incr
        if current_index >= len(rules_ct):
            not_repeated = False
            finish = True
        elif rules_ct[current_index] != 0:
            not_repeated = False
        else:
            rules_ct[current_index] = 1
    return accum, finish


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''find the value of accumulator before the process repeats'''
    # there must be a better regex way to handle the rstrip('\n')
    rules = [re.split(r"[\s]", line.rstrip('\n')) for line in input_file]
    accum, finish = run_iteration(rules)
    assert not finish
    return accum


def switch_index(rules_, index_change):
    '''switch the jmp or nop at that index'''
    rules_2 = copy.deepcopy(rules_)
    if rules_[index_change][0] == 'jmp':
        rules_2[index_change][0] = 'nop'
    else:
        rules_2[index_change][0] = 'jmp'
    return rules_2


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''one nop->jmp or one jmp->nop which one'''
    # i'm just going to loop thru all jmps...there must be a better way to do....

    # there must be a better regex way to handle the rstrip('\n')
    rules = [re.split(r"[\s]", line.rstrip('\n')) for line in input_file]

    to_switch = [idx for idx, element in enumerate(rules)
                 if element[0] == 'jmp']

    # now switch the index
    for idx in to_switch:
        rules_switched = switch_index(rules, idx)
        # now run again
        accum, finish = run_iteration(rules_switched)
        if finish:
            break
    return accum
