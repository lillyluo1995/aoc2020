from typing import IO

def read_file(input_file):
    '''read the passport data since its kinda funky'''
    data = input_file.read()
    answers = data.split('\n\n')
    return answers

def p_1(input_file: IO,
        debug=False): # pylint: disable=unused-argument
    '''find how many questions each group answered yes to then sum by group'''
    answers = read_file(input_file)
    output = 0
    for answer in answers:
        answer = answer.replace('\n', '') #first strip the newlines
        output += len(set(answer))
    return output

def p_2(input_file: IO,
        debug=False): # pylint: disable=unused-argument
    '''find how many questions each person in each
    group answered yes to then sum by group'''
    answers = read_file(input_file)
    output = 0
    for answer in answers:
        by_person = answer.split('\n')
        by_person_set = [set(person) for person in by_person]
        output += len(set.intersection(*by_person_set))
    return output
