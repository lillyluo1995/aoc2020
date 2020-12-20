from typing import IO
from itertools import product


def parse(input_file, dims):
    '''read the input file'''
    input_array = [list(x.replace('\n', '')) for x in input_file.readlines()]
    state = {}
    for x_idx, row in enumerate(input_array):
        for y_idx, col in enumerate(row):
            state_tup = [x_idx, y_idx]
            for _ in range(dims-len(state_tup)):
                state_tup.append(0)
            if col == '#':
                state[tuple(state_tup)] = 1
            else:
                state[tuple(state_tup)] = 0
    return state


def get_neighbor_tuples(current_coord):
    '''get the neighbors coords'''
    dims = len(current_coord)
    neighbors = [tuple(map(sum, zip(current_coord, step)))
                 for step in product([-1, 0, 1], repeat=dims)]
    neighbors = [
        neighbor for neighbor in neighbors if neighbor != current_coord]
    return neighbors


def add_neighbors(state):
    '''get all the new points that we might need to parse over'''
    empty_state = state.copy()
    for location, _ in state.items():
        neighbors = get_neighbor_tuples(location)
        for neighbor in neighbors:
            if neighbor not in state:
                empty_state[neighbor] = 0
    return empty_state


def print_state(state):
    '''print out the current state for debugging...only works for 3 dim'''
    all_tuples = list(state.keys())
    min_x, min_y, min_z = [min([tup[i] for tup in all_tuples])
                           for i in range(3)]
    max_x, max_y, max_z = [max([tup[i] for tup in all_tuples])
                           for i in range(3)]

    for z_idx in range(min_z, max_z+1):
        print('z={z}'.format(z=z_idx))
        for x_idx in range(min_x, max_x+1):
            row = []
            for y_idx in range(min_y, max_y+1):
                row.append(str(state[(x_idx, y_idx, z_idx)]))
            print(''.join(row))
        print('\n')


def iterate(state):
    '''move from one state to the next'''
    empty_state = add_neighbors(state)
    new_state = empty_state.copy()
    for location, value in empty_state.items():
        neighbors = get_neighbor_tuples(location)
        num_active_neighbors = 0
        for neighbor in neighbors:
            if neighbor in empty_state:
                num_active_neighbors += empty_state[neighbor]
        if value == 1:
            if num_active_neighbors not in [2, 3]:
                new_state[location] = 0
        else:
            if num_active_neighbors == 3:
                new_state[location] = 1
    return new_state


def count_active(state):
    '''count number of active states'''
    return sum([value for _, value in state.items()])


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''return number of active states with 3 dimensions'''
    num_iter = 6
    dims = 3
    current = parse(input_file, dims)
    for _ in range(num_iter):
        current = iterate(current)
    return count_active(current)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''return number of active states with 3 dimensions'''
    num_iter = 6
    dims = 4
    current = parse(input_file, dims)
    for _ in range(num_iter):
        current = iterate(current)
    return count_active(current)
