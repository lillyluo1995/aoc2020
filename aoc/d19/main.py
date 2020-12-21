from typing import IO
import re


def read_file(input_file):
    '''parse the file into the rules and the messages'''
    rules = {}
    messages = []
    rules_group = True
    for line in input_file.readlines():
        if rules_group:
            group = re.findall(r"[0-9]+|\||a|b", line)
            if len(group) > 0:
                rules[group[0]] = group[1:]
        else:
            messages.append(line.strip())
        if line == '\n':
            rules_group = False
    return rules, messages


def make_rule(rules, idx):
    '''clearly spell out rules of idx'''
    if idx == '|':
        return '|'
    rule = rules[idx]
    if rule in [['a'], ['b'], ['|']]:
        return rule[0]
    regex_str = ''
    for req in rule:
        new_format = make_rule(rules, req)
        if '|' in new_format and len(new_format) > 1:
            regex_str = regex_str+'({f})'.format(f=new_format)
        else:
            regex_str = regex_str + new_format
    return regex_str


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''check number of messages that fit rule 0'''
    rules, messages = read_file(input_file)
    regex_rule = make_rule(rules, '0')

    good_messages = 0
    for message in messages:
        good_messages += bool(re.fullmatch(regex_rule, message))
    return good_messages


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''now replace rules 8 and 11 and becomes cyclical...'''
    # row the rules are cyclical....basically
    # rule 8 becomes 42|42|42.... so (42)+ and rule 11 becomes
    # (42|42|42....)(31|31|31|...) so (42){i}(31){i} where i increments. i
    # arbitrarily sent the top of i as 10
    rules, messages = read_file(input_file)
    rules['8'] = '({rule})+'.format(rule=make_rule(rules, '42'))

    good_messages = 0
    for incr in range(1, 10):
        rules['11'] = '({rule1}){{{incr}}}({rule2}){{{incr}}}'.format(
            rule1=make_rule(rules, '42'), rule2=make_rule(rules, '31'),
            incr=incr)

        regex_rule = rules['8']+rules['11']
        for message in messages:
            good_messages += \
                bool(re.fullmatch(regex_rule, message))
    return good_messages
