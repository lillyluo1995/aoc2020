from typing import IO
import re
import numpy as np

def read_file(input_file):
    '''parse thru the file and return a dict of dicts'''
    tiles = {}
    current_tile = 0
    for line in input_file.readlines():
        tile_str = re.findall('Tile|[0-9]+', line)
        if tile_str:
            _, current_tile = tile_str
            current_tile = int(current_tile)
            tiles[current_tile] = []
        else:
            if line == '\n':
                continue
            new_line = []
            line = line.strip()
            for char in line:
                if char == '#':
                    new_line.append('1')
                else:
                    new_line.append('0')
            tiles[current_tile].append(new_line)
    return tiles

def print_tile(tiles, tile_num):
    '''print out the tiles for ease of debugging'''
    if not tile_num: #we're printing them all out:
        for tile, _ in tiles.items():
            print_tile(tiles, tile)
    else:
        tile_detail = tiles[tile_num]
        print('TILE={tile_num}'.format(tile_num=tile_num))
        for line in tile_detail:
            print(line)
        print('\n')

def return_id(line):
    '''get the idx mapping of the line'''
    return int(''.join(line),2)

def get_indices(tile, tile_dir):
    '''get the indices in the specified direction'''
    output = []
    if tile_dir == 'top':
        output = tile[0]
    elif tile_dir == 'bottom':
        output = tile[-1]
    elif tile_dir == 'left':
        output = [row[0] for row in tile]
    else: #right
        output = [row[-1] for row in tile]
    return output

def find_corner_pieces(tile_placement, tile_id_reverse):
    '''basically find the tiles with 2 unique edge sides'''
    #get a list of all the values that show up and # of times
    edge_table = {}
    for _, edges in tile_placement.items():
        for _, edge in edges.items():
            if edge in edge_table:
                edge_table[edge] += 1
            else:
                edge_table[edge] = 1

            if tile_id_reverse[edge] in edge_table:
                edge_table[tile_id_reverse[edge]] += 1
            else:
                edge_table[tile_id_reverse[edge]] = 1

    #get a list of the edges that only show up once
    unique_edges = set()
    for edge, number in edge_table.items():
        edge_reverse = edge_table[tile_id_reverse[edge]]
        if number == 1 and edge_reverse == 1:
            unique_edges.add(edge)

    #now find the tiles the correspond to the edges that only have 1...
    #i'll also check the reverse of the edges...
    corners = set()
    for tile, edges in tile_placement.items():
        num_unique = 0
        for edge in edges.values():
            if edge in unique_edges:
                num_unique += 1
        if num_unique > 1:
            corners.add(tile)
    return corners

def p_1(input_file: IO,
        debug=False): # pylint: disable=unused-argument
    '''get the product of the corner tile numbers'''
    tiles = read_file(input_file)
    tile_placement = {}
    tile_id_reverse = {}
    for tile_num, tile in tiles.items():
        tile_placement[tile_num] = {}
        for tile_dir in ['top', 'bottom', 'left', 'right']:
            line = get_indices(tile, tile_dir)[:]
            tile_id = return_id(line)
            tile_placement[tile_num][tile_dir]=tile_id

            line.reverse()
            reversed_tile_id = return_id(line)
            tile_id_reverse[tile_id] = reversed_tile_id
            tile_id_reverse[reversed_tile_id] = tile_id
    corners = find_corner_pieces(tile_placement, tile_id_reverse)
    return np.prod(list(corners))



def p_2(input_file: IO,
        debug=False): # pylint: disable=unused-argument
    '''find the # that aren't part of the sea monster....'''
    print(read_file(input_file))
