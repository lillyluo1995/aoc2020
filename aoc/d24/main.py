from typing import IO
import re
import sympy

DIRECTION = {
    'e': 0,
    'ne': sympy.pi/3,
    'nw': 2*sympy.pi/3,
    'w': sympy.pi,
    'sw': 4*sympy.pi/3,
    'se': 5*sympy.pi/3
}

ALL_DIR = ['e', 'w', 'ne', 'nw', 'se', 'sw']

def mapping_to_loc(mapping):
    '''mapping to location'''
    (x_coord,y_coord) = (0,0)
    for dir_, number in mapping.items():
        (x_coord,y_coord) = (x_coord+number * sympy.cos(DIRECTION[dir_]), \
            y_coord+number*sympy.sin(DIRECTION[dir_]))
    return (x_coord,y_coord)

def initialize_floor(input_file):
    '''initialize the floor into a location map 1 for black 0 for white'''
    location_map = {}
    regex_str = '|'.join(ALL_DIR)
    for line in input_file.readlines():
        dirs = re.findall(regex_str, line.strip())
        dir_map = {dir_:dirs.count(dir_) for dir_ in ALL_DIR}
        loc = mapping_to_loc(dir_map)
        if loc in location_map:
            if location_map[loc] == 1:
                location_map[loc] = 0
            else:
                location_map[loc] = 1
        else:
            location_map[loc] = 1
    return location_map

def p_1(input_file: IO,
        debug=False): # pylint: disable=unused-argument
    '''how many tiles are black
    467 too high'''
    location_map = initialize_floor(input_file)
    return sum(list(location_map.values()))

NEIGHBORS = [(sympy.cos(DIRECTION[dir_]), sympy.sin(DIRECTION[dir_]) )for dir_ in ALL_DIR]

def get_neighbors(coord):
    '''given a coordinate, return the neighbors we need to check'''
    return [(coord[0] + neighbor[0], coord[1] + neighbor[1]) \
        for neighbor in NEIGHBORS]

def flip(location_map):
    '''flip the relevant ones...'''
    #add neighbors
    expanded_location_map = location_map.copy()
    for location, _ in location_map.items():
        neighbors = get_neighbors(location)
        for neighbor in neighbors:
            if neighbor not in expanded_location_map:
                expanded_location_map[neighbor] = 0

    #now flip the relevant ones...
    final_location_map = expanded_location_map.copy()
    for location, color in expanded_location_map.items():
        neighbors = get_neighbors(location)
        num_black = 0
        for neighbor in neighbors:
            if neighbor in expanded_location_map:
                num_black += expanded_location_map[neighbor]
        if color == 1 and num_black == 0:
            final_location_map[location] = 0
        if color == 1 and num_black > 2:
            final_location_map[location] = 0
        elif color ==0 and num_black == 2:
            final_location_map[location] = 1
    return final_location_map

def p_2(input_file: IO,
        debug=False): # pylint: disable=unused-argument
    '''flip tile colors per rules'''
    location_map = initialize_floor(input_file)
    for num in range(100):
        print(num)
        location_map = flip(location_map)
    return sum(list(location_map.values()))
