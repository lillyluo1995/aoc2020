from typing import IO
import re
from collections import deque


def read_line(input_file):
    '''parse the inputs into an array of chars'''
    lines = []
    for line in input_file.readlines():
        inputs = deque(re.findall(r"[0-9]|\+|\*|\(|\)", line))
        lines.append(inputs)
    return lines


def run_operators(numbers, operators):
    '''given stack of operators and numbers, let's run thru'''
    print(len(operators), len(numbers))
    assert len(numbers)-1 == len(operators)
    total = numbers.popleft()
    while numbers:
        current = numbers.popleft()
        operator = operators.popleft()
        if operator == '+':
            total += current
        elif operator == '*':
            total *= current
    return total


def rpn_1(line):
    '''put line into reverse polish notation'''
    output = deque()
    operators = deque()

    num_regex = re.compile('[0-9]+')
    operator_regex = re.compile(r"\+|\*")
    while line:
        head = line.popleft()
        if num_regex.match(head) is not None:
            output.append(int(head))
        elif operator_regex.match(head) is not None:
            while operators:
                op_head = operators.pop()
                if op_head == '(':
                    operators.append(op_head)
                    break
                output.append(op_head)
            operators.append(head)
        else:  # it's a parenthesis
            if head == '(':  # left parent
                operators.append(head)
            else:  # right parent
                while operators:
                    op_head = operators.pop()
                    if op_head == '(':
                        break
                    output.append(op_head)
    if operators:
        op_head = operators.pop()
        output.append(op_head)
    return output


def parse_rpn(rpn_input):
    '''given rpn input, output the actual #'''
    int_list = deque()
    while len(rpn_input) > 0:
        head = rpn_input.popleft()
        if head in ['+', '*']:
            int1 = int_list.pop()
            int2 = int_list.pop()
            if head == '+':
                int_list.append(int1+int2)
            else:
                int_list.append(int1*int2)
        else:
            int_list.append(head)
    return int_list[0]


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''solve as left to right and parenthesis but no pemdas'''
    inputs = read_line(input_file)
    total_sum = 0
    for line in inputs:
        rpn_input = rpn_1(line)
        total_sum += parse_rpn(rpn_input)
    return total_sum


MAPPING = {
    '+': 1,
    '*': 0
}


def rpn_2(line):
    '''put line into reverse polish notation'''
    output = deque()
    operators = deque()

    num_regex = re.compile('[0-9]+')
    operator_regex = re.compile(r"\+|\*")
    while line:
        head = line.popleft()
        if num_regex.match(head) is not None:
            output.append(int(head))
        elif operator_regex.match(head) is not None:
            while operators:
                op_head = operators.pop()
                if op_head == '(':
                    operators.append(op_head)
                    break
                if MAPPING[op_head] < MAPPING[head]:
                    operators.append(op_head)
                    break
                output.append(op_head)
            operators.append(head)
        else:  # it's a parenthesis
            if head == '(':  # left parent
                operators.append(head)
            else:  # right parent
                while operators:
                    op_head = operators.pop()
                    if op_head == '(':
                        break
                    output.append(op_head)
    while operators:
        op_head = operators.pop()
        output.append(op_head)
    return output


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''solve as left to right but addition > mult'''
    inputs = read_line(input_file)
    total_sum = 0
    for line in inputs:
        rpn_input = rpn_2(line)
        total_sum += parse_rpn(rpn_input)
    return total_sum
