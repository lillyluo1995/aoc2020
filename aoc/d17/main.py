from typing import IO
import copy
import numpy as np



def read_file(input_file):
    '''read the input file'''
    return np.array([list(x.replace('\n', '')) for x in input_file.readlines()])


def print_state(current_state):
    '''print out the current state for debugging'''
    num_layers = len(current_state)
    deincrement = int((num_layers-1)/2)
    for idx, layer in enumerate(current_state):
        print('z={z}'.format(z=idx-deincrement))
        for row in layer:
            print(''.join(row))
        print('\n')


def initiate_next(current_state):
    '''instantiate the next one empty'''
    num_rows, num_cols = len(current_state[0]), len(current_state[0][0])
    # first we'll add the layers and shift accordingly...
    new_state = copy.deepcopy(current_state)
    for idx, layer in enumerate(current_state):
        # add columns
        new_col = ['.']*len(layer)
        temp_new = np.vstack((new_col, layer, new_col))
        # add rows
        new_row = np.array(['.']*len(temp_new))[np.newaxis]
        new_row = np.transpose(new_row)
        new_state[idx] = np.hstack((new_row, temp_new, new_row))

    # now add the row and shift....
    new_state.insert(0, np.array([['.']*(num_cols+2)]*(num_rows+2)))
    new_state.append(np.array([['.']*(num_cols+2)]*(num_rows+2)))
    return new_state


def check_neighbors(current_state, current_coord):
    '''count how many active neighbors a cell has'''
    num_active = 0

    # since we appended one row, col, and layer to the beginning for all
    for z_chg in [-1, 0, 1]:
        for x_chg in [-1, 0, 1]:
            for y_chg in [-1, 0, 1]:
                if abs(z_chg)+abs(x_chg)+abs(y_chg) == 0:
                    continue
                if current_coord[0]+z_chg > len(current_state)-1 \
                    or current_coord[1]+x_chg > len(current_state[0])-1 \
                        or current_coord[2]+y_chg > len(current_state[0][0])-1:
                    continue  # if out of bounds, deffo not active

                neighbor = \
                    current_state[current_coord[0] +
                                    z_chg][current_coord[1]+x_chg][current_coord[2]+y_chg]
                if neighbor == '#':
                    num_active += 1
    return num_active


def iteration(current_state):
    '''iterate the current state'''
    z_start, x_start, y_start = len(current_state), len(current_state[0]), \
        len(current_state[0][0])
    empty = initiate_next(current_state)
    next_empty = copy.deepcopy(empty)
    for z_c in range(z_start+2):
        for x_c in range(x_start+2):
            for y_c in range(y_start+2):
                current = empty[z_c][x_c][y_c]
                num_active_neighbors = check_neighbors(empty, [z_c, x_c, y_c])
                if current == '#':
                    if num_active_neighbors not in [2, 3]:
                        next_empty[z_c][x_c][y_c] = '.'
                else:
                    if num_active_neighbors == 3:
                        next_empty[z_c][x_c][y_c] = '#'
    return next_empty


def count_active(current_state):
    '''count number of active states'''
    num_active = 0
    for z_coord, _ in enumerate(current_state):
        for x_coord, _ in enumerate(current_state[0]):
            for y_coord, _ in enumerate(current_state[0][0]):
                if current_state[z_coord][x_coord][y_coord] == '#':
                    num_active += 1
    return num_active


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''preallocate the space....'''
    num_iter = 6

    current = [read_file(input_file)]
    for cyc in range(num_iter):
        print('CYCLE NUMBER = {cyc}'.format(cyc=cyc+1))
        current = iteration(current)
    return count_active(current)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''do part 2'''
    pass
