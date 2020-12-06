from typing import IO
import re

def read_file(input_file):
    '''read the passport data since its kinda funky'''
    data = input_file.read()
    passport_data = data.split('\n\n')
    return passport_data

def verify_passport_1(passport, cid_optional):
    '''check if the passport has the necessary fields...
    if cid is optional, then don't require cid'''
    fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    if not cid_optional:
        fields += 'cid'
    res = re.split(':| |\n', passport)
    valid = True
    for field in fields:
        if field not in res:
            valid = False
    return valid


def check_year(field, value):
    '''check if birth, issue, and expiration year are valid'''
    valid = True
    limits = {
        'byr': [1920, 2002],
        'iyr': [2010, 2020],
        'eyr': [2020, 2030],
    }
    if len(value) != 4:
        valid = False
    else:
        value_dbl = int(value)
        if limits[field][0] > value_dbl or limits[field][1] < value_dbl:
            valid = False
    return valid


def check_height(value):
    '''check if height is valid'''
    valid = True
    limits = {
        'cm': [150, 193],
        'in': [59, 76]
    }
    units = value[-2:]
    if units not in ['cm', 'in']:
        valid = False
    else:
        height = int(value[:len(value)-2])
        if limits[units][0] > height \
                or limits[units][1] < height:
            valid = False
    return valid


def check_hair(value):
    '''check if hair color is valid'''
    valid = True
    hcl = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'a', 'b', 'c', 'd', 'e', 'f'}
    if value[0] != '#':
        valid = False
    else:
        remaining = set(value[1:])
        if len(remaining.intersection(hcl)) != len(remaining):
            valid = False
    return valid


def check_eye(value):
    '''check if eye color is valid'''
    ecl = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
    if value not in ecl:
        return False
    return True


def check_field_valid(field, value):
    '''check if the value for a field is good. both str to start'''
    valid = True
    # first check if all the fields are there

    # how do i reduce number of branches here?
    if field in ['byr', 'iyr', 'eyr']:
        valid = check_year(field, value)
    elif field == 'hgt':
        valid = check_height(value)
    elif field == 'hcl':
        valid = check_hair(value)
    elif field == 'ecl':
        valid = check_eye(value)
    elif field == 'pid':
        if len(value) != 9:
            valid = False
    return valid


def verify_passport_2(passport, cid_optional):
    '''check if the passport has the necessary fields...
    if cid is optional, then don't require cid'''
    fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    if not cid_optional:
        fields += 'cid'
    res = re.split(':| |\n', passport)

    valid = True
    for field in fields:
        try:
            field_index = res.index(field)
            value = res[field_index+1]
            if not check_field_valid(field, value):
                valid = False
        except:  # pylint: disable=W0702
            valid = False
    return valid


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''check how many passports have all the required fields
    #except country id'''
    passport_data = read_file(input_file)
    valid_passports = 0
    for passport in passport_data:
        valid_passports += verify_passport_1(passport, True)
    return valid_passports


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''check how many passports have all the required fields
    #except country id AND have valid inputs'''
    passport_data = read_file(input_file)
    valid_passports = 0
    for passport in passport_data:
        valid_passports += verify_passport_2(passport, True)
    return valid_passports
