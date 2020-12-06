from typing import IO

def traverse(forest, right, down):
    '''traverse forest starting at top left, then go number of squares
    right and number of squares down'''
    num_orig = len(forest[0])  # after this many, it starts to rpt
    num_spots = len(forest)  # how many til bottom

    # this can be better, i only need to allocate
    # num_spots/down number of spots...but it doesnt work
    # allocation error...to fix later.
    sleigh_pts = ['x']*num_spots
    column = 0
    for row_num, row_content in enumerate(forest):
        if row_num % down == 0:
            sleigh_pts[row_num] = row_content[column % num_orig]
            column += right
    return sleigh_pts.count('#')


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''given the input, see how many trees we collide w'''
    forest = [line.rstrip('\n') for line in input_file]
    return traverse(forest, 3, 1)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''now, we're going to have diff ways of traversing...
    what's the product of the # trees we hit on each traverse'''
    paths = [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]
    forest = [line.rstrip('\n') for line in input_file]

    num_trees = 1
    for path in paths:
        num_trees *= traverse(forest, path[0], path[1])
    return num_trees
