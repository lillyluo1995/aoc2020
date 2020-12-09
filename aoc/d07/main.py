from typing import IO
import re
from collections import deque


def parse_line(line):
    '''given a line, split it into the important stuff
    i assume the order will always be x x bags contains num x x....'''
    bagofwords = re.split(r"[\s.,]", line)
    # there must be a better way to do the below via regex...
    bagofwords = [x for x in bagofwords if len(x) > 0]
    return bagofwords


def bfs(mapping, root):
    '''count number of children in tree starting at root'''
    queue_ = deque()
    seen = set()

    queue_.append(root)
    num_children = 0
    while queue_:
        head = queue_.popleft()

        if head in mapping:
            for parent in mapping[head]:
                if parent in seen:
                    continue
                if parent not in queue_:
                    queue_.append(parent)
                    num_children += 1
        seen.add(head)
    return num_children

def dfs(mapping, root):
    '''dfs to find number of children but need to scale by multiple'''
    queue_ = deque()
    queue_.append(root)

    num_bags = {}
    num_bags[root] = 0
    while queue_:
        head = queue_.pop()  # head is the color
        children = mapping[head]
        if not children:
            num_bags[head] = 0
        else:
            for child in children:
                num_bags[head] += child[1] +\
                    dfs(mapping, child[0])*child[1]
    return num_bags[root]

def words_to_node(words):
    '''given an array of words, turn it into a node....
    assume that it follows the rule:
    x x bags contain # x x bags # x x  bags ....
    0 1 2    3       4 5 6 7    8 9 10 11'''
    parent_color = ' '.join(words[0:2])
    children_phrase = words[4:]

    if len(children_phrase) == 3:  # no other bags = 3, 1 x x bag = 4
        return parent_color, []
    num_children = int(len(children_phrase)/4)
    children = [(' '.join(children_phrase[4*i+1:4*i+3]),
                int(children_phrase[4*i])) for i in range(num_children)]
    return parent_color, children

def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''given a set of rules, how many bags can i use to carry
    my shiny gold bag? '''

    def parse(input_file):
        '''returns map of child -> parent'''
        mapping = {}
        for line in input_file.readlines():
            phrase = parse_line(line)
            parent_color, children = words_to_node(phrase)
            for child, _ in children:
                if child in mapping:
                    if parent_color not in mapping[child]:
                        mapping[child].append(parent_color)
                else:
                    mapping[child] = [parent_color]
        return mapping
    mapping = parse(input_file)

    # now this is the root of my tree and i'm going to see how
    # many children it has
    return bfs(mapping, 'shiny gold')

def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''how many bags will my shiny gold bag be req'd to hold?'''

    def parse(input_file):
        '''returns map of parent -> child'''
        mapping = {}
        for line in input_file.readlines():
            phrase = parse_line(line)
            parent_color, children = words_to_node(phrase)
            mapping[parent_color] = children
        return mapping
    mapping = parse(input_file)

    # now this is the root of my tree and i'm going to see how
    # many children it has
    return dfs(mapping, 'shiny gold')
