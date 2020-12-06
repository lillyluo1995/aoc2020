from typing import IO


def password_valid_1(rule):
    '''check if rule (with the rule and password) if valid'''
    [req, password] = rule.split(': ')
    [nums, letter] = req.split(' ')
    [min_, max_] = [int(x) for x in nums.split('-')]

    # check if the number of times letter occurs in
    # password is btw min and max
    num_times = password.count(letter)
    if min_ <= num_times <= max_:
        return True
    return False


def password_valid_2(rule):
    '''check if rule (with the rule and password) if valid'''
    [req, password] = rule.split(': ')
    [nums, letter] = req.split(' ')
    [i_1, i_2] = [int(x) for x in nums.split('-')]

    outputs = [password[i_1-1], password[i_2-1]]  # subtract 1 bc 0 index
    if outputs.count(letter) == 1:
        return True
    return False


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''given a list of rules/passwords, return the number of valid passwords'''
    rules = [line.rstrip('\n') for line in input_file]
    valid = [1 for rule in rules if password_valid_1(rule)]
    return sum(valid)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''given a list of rules/passwords, return the number of valid passwords'''
    rules = [line.rstrip('\n') for line in input_file]
    valid = [1 for rule in rules if password_valid_2(rule)]
    return sum(valid)
