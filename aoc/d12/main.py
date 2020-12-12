from typing import IO
import re
import math

MAPPING = {
    'N': (0, 1),
    'S': (0, -1),
    'E': (1, 0),
    'W': (-1, 0),
    'L': 1,  # clockwise
    'R': -1  # counterclockwise
}


def read_file(input_file):
    '''read the input file of instructions'''
    regex_instr = re.compile('([A-Z])([0-9]+)')
    directions = [regex_instr.match(x).groups()
                  for x in input_file.readlines()]

    # need to use yield as here to be more efficient...
    directions = [(x[0], int(x[1])) for x in directions]
    return directions


def add_tuple(tuple_1, tuple_2):
    '''add tuple_1 and tuple_2'''
    return tuple(map(sum, zip(tuple_1, tuple_2)))


def mult_tuple(tuple_, scalar_):
    '''multiple tuple_ by scalar_'''
    return tuple([int(round(scalar_*x, 0)) for x in tuple_])


def get_current_angle(start_dir):
    '''get the angle based on the start/end coord...this is basically only 90 angles'''
    if start_dir == (0, 0):
        current_angle = 0
    elif start_dir[0] == 0:
        if start_dir[1] > 0:
            current_angle = math.pi/2
        elif start_dir[1] < 0:
            current_angle = -math.pi/2
    elif start_dir[1] == 0:
        if start_dir[0] > 0:
            current_angle = 0
        elif start_dir[0] < 0:
            current_angle = -math.pi
    else:
        current_angle = math.atan(start_dir[1]/start_dir[0])
        if start_dir[0] < 0:
            current_angle = math.pi+current_angle
    return current_angle


def interpret_dir(start_coord, start_dir, direction):
    '''given the starting coordinate/direction and an instruction, return the
    next location of the ship'''
    dir_, num_ = direction
    end_dir = start_dir
    current_angle = get_current_angle(start_dir)

    if dir_ == 'F':
        end_coord = add_tuple(start_coord, mult_tuple(start_dir, num_))
    elif dir_ in ['N', 'S', 'E', 'W']:
        end_coord = add_tuple(start_coord, mult_tuple(MAPPING[dir_], num_))
    elif dir_ in ['L', 'R']:
        num_rad = num_*math.pi/180
        end_dir = (int(round(math.cos(current_angle+MAPPING[dir_]*num_rad),0)),
                   int(round(math.sin(current_angle+MAPPING[dir_]*num_rad),0)))
        end_coord = start_coord
    return end_coord, end_dir


def interpret_dir_waypoint(coord_, waypoint, direction):
    '''given the starting coordinate/direction and an instruction, return the
    next location of the ship'''
    dir_, num_ = direction

    # moves ship
    if dir_ == 'F':
        coord_ = add_tuple(coord_, mult_tuple(waypoint, num_))
    # moves relative direction of waypoint relative to ship
    elif dir_ in ['N', 'S', 'E', 'W']:
        waypoint = add_tuple(waypoint, mult_tuple(MAPPING[dir_], num_))
    # moving the waypoint around the ship, ship in meme place
    elif dir_ in ['L', 'R']:
        num_rad = num_*math.pi/180
        waypoint_ship_angle = get_current_angle((waypoint[0], waypoint[1]))
        waypoint_ship_dist = math.sqrt(math.pow(waypoint[0], 2) +
                                       math.pow(waypoint[1], 2))
        new_waypoint_ship_vector = (math.cos(waypoint_ship_angle+MAPPING[dir_]*num_rad),
                                    math.sin(waypoint_ship_angle+MAPPING[dir_]*num_rad))
        waypoint = mult_tuple(new_waypoint_ship_vector, waypoint_ship_dist)
    return coord_, waypoint


def get_manhattan_distance(coord):
    '''get the manhattan distance of a coordinate'''
    return int(abs(coord[0])+abs(coord[1]))


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''what is the manhattan distance of my boat to the starting point?
    #guess 1 - 1753 too high'''
    directions = read_file(input_file)
    coord_, dir_ = (0, 0), (1, 0)
    for direction in directions:
        coord_, dir_ = interpret_dir(coord_, dir_, direction)
    return get_manhattan_distance(coord_)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''what is the manhattan distance of my boat using this waypoint?
    #guess 1 - 1514116849 too high
    #guess 2 - 7680 too low'''
    directions = read_file(input_file)
    coord_, waypoint_coord = (0, 0), (10, 1)
    for direction in directions:
        coord_, waypoint_coord = interpret_dir_waypoint(
            coord_, waypoint_coord, direction)
    return get_manhattan_distance(coord_)
