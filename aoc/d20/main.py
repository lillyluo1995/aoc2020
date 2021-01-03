from typing import IO
import re
import numpy as np


DIRECTIONS = ['top', 'bottom', 'left', 'right']
PARENT_MAPPING = {
    'top': 'bottom',
    'left': 'right',
    'right': 'left',
    'bottom': 'top'
}


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


def print_tile(tile):
    '''print out a singular tile'''
    for line in tile:
        print(''.join(line))
    print('\n')


def print_tiles(tiles, tile_num):
    '''print out the tiles for ease of debugging'''
    if not tile_num:  # we're printing them all out:
        for tile in tiles.values():
            print_tile(tile)
    else:
        tile_detail = tiles[tile_num]
        print('TILE={tile_num}'.format(tile_num=tile_num))
        print_tile(tile_detail)


def return_id(line):
    '''get the idx mapping of the line'''
    return int(''.join(line), 2)


def get_indices(tile, tile_dir):
    '''get the indices in the specified direction'''
    output = []
    if tile_dir == 'top':
        output = tile[0]
    elif tile_dir == 'bottom':
        output = tile[-1]
    elif tile_dir == 'left':
        output = [row[0] for row in tile]
    else:  # right
        output = [row[-1] for row in tile]
    return output


def get_edge_keys(tiles):
    '''get a mapping of edge key -> tile number and edge key -> reversed'''
    edge_key = {}  # map from edge key to tile number
    reverse_edge = {}  # map from edge key to the edge key reversed
    for tile_num, tile in tiles.items():
        for tile_dir in DIRECTIONS:
            line = get_indices(tile, tile_dir)[:]
            edge_id = return_id(line)
            if edge_id in edge_key:
                edge_key[edge_id].add(tile_num)
            else:
                edge_key[edge_id] = set([tile_num])

            line.reverse()
            reverse_id = return_id(line)
            reverse_edge[edge_id] = reverse_id
            reverse_edge[reverse_id] = edge_id
    return edge_key, reverse_edge


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''get the product of the corner tile numbers'''
    tiles = read_file(input_file)
    edge_key, reverse_edge = get_edge_keys(tiles)

    # ok now find the edges in which both itself OR its reverse only occur once..
    eligible_corners = set()
    eligible_edges = set()
    for edge_id, values in edge_key.items():
        relevant_tiles = set(values)
        if reverse_edge[edge_id] in edge_key:
            relevant_tiles = relevant_tiles & edge_key[reverse_edge[edge_id]]
        if len(relevant_tiles) == 1:
            tile = list(relevant_tiles)[0]
            if tile in eligible_edges:
                eligible_corners.add(tile)
            else:
                eligible_edges.add(tile)
    return np.prod(list(eligible_corners))


def rotate_tile(tile):
    '''rotate the tile clockwise 90'''
    return np.rot90(tile)


def flip_tile(tile, horizontal=False):
    '''flip the tile vertically or horizontally'''
    if horizontal:
        return np.flip(tile, axis=1)
    return np.flip(tile, axis=0)


def get_orientations(tile):
    '''rotate the tile all ways...'''
    orientations = [tile, flip_tile(tile)]
    for _ in range(3):
        tile = rotate_tile(tile)
        orientations.append(tile)
        orientations.append(flip_tile(tile))
        orientations.append(flip_tile(tile, horizontal=True))
    return orientations


def get_parent_tile(img, parent_position, max_y, max_x):
    '''get the parent time from the img given the starting position'''
    parent_tile = []
    for y_incr in range(max_y):
        row = []
        for x_incr in range(max_x):
            row.append(
                img[(parent_position[0]+x_incr, parent_position[1]-y_incr)])
        parent_tile.append(row)
    return parent_tile


def get_oriented_tile(orientations, parent_edge_id, parent_dir):
    '''orientations is a single tile rotated and flipped all ways possible.
    this function returns the correct orientation of the tile s.t. it matches the
    parent edge id on the side directed by parent_dir'''
    for tile_position in orientations:
        tile_target_edge = return_id(get_indices(
            tile_position, PARENT_MAPPING[parent_dir]))
        if tile_target_edge == parent_edge_id:
            return tile_position
    return None


def get_placement(tile, reverse_edge, parent_position, img):
    '''return the tile in the correct orientation and the top left of the tile
    so that it is adjacent to the parent'''
    parent_tile = get_parent_tile(
        img, parent_position, len(tile), len(tile[0]))
    x_shift_size, y_shift_size = len(tile[0]), len(tile)
    for parent_dir in DIRECTIONS:
        parent_edge_id = return_id(get_indices(parent_tile, parent_dir))
        for child_dir in DIRECTIONS:
            child_edge_id = return_id(get_indices(tile, child_dir))
            if parent_edge_id in \
                    [return_id(get_indices(tile, child_dir)), reverse_edge[child_edge_id]]:
                orientations = get_orientations(tile)
                if parent_dir == 'left':
                    position = (parent_position[0] -
                                x_shift_size, parent_position[1])
                    return position, get_oriented_tile(orientations, parent_edge_id, parent_dir)
                if parent_dir == 'right':
                    position = (parent_position[0] +
                                x_shift_size, parent_position[1])
                    return position, get_oriented_tile(orientations, parent_edge_id, parent_dir)
                if parent_dir == 'bottom':
                    position = (parent_position[0],
                                parent_position[1]-y_shift_size)
                    return position, get_oriented_tile(orientations, parent_edge_id, parent_dir)
                if parent_dir == 'top':
                    position = (parent_position[0],
                                parent_position[1]+y_shift_size)
                    return position, get_oriented_tile(orientations, parent_edge_id, parent_dir)
    print('we got an issue')
    return None, None


def get_neighbors(tile_num, tiles, edge_key, reverse_edge):
    '''get neighbors of this tile_num'''
    neighbors = set()
    tile = tiles[tile_num]
    for dir_ in DIRECTIONS:
        edge_id = return_id(get_indices(tile, dir_))
        reverse_edge_id = reverse_edge[edge_id]
        if edge_id in edge_key:
            neighbors = neighbors | edge_key[edge_id]
        if reverse_edge_id in edge_key:
            neighbors = neighbors | edge_key[reverse_edge_id]
    if tile_num in neighbors:
        neighbors.remove(tile_num)
    return neighbors


def build_image(tiles, edge_key, reverse_edge):
    '''build the image....'''

    img = {}  # mapping of (x,y) -> # or . the final img
    positions = {}  # mapping of tile -> x,y coordinate for top left
    visited = set()

    def dfs(tile_num, parent_num=None):
        '''use dfs to add the things by neighbor'''

        def visit():
            '''visit a tile...and process and put it into the image correctly'''
            if parent_num is None:
                # this is the first tile i'm placing
                position = (0, 0)
                tile = tiles[tile_num]
            else:
                parent_position = positions[parent_num]
                position, tile = \
                    get_placement(tiles[tile_num],
                                  reverse_edge, parent_position, img)

            # ok now that i have the location of the top left of the tile,
            # i'm going to place the tile correctly in the img
            for y_incr, row in enumerate(tile):
                for x_incr, value in enumerate(row):
                    img[(position[0]+x_incr, position[1]-y_incr)] = value
            positions[tile_num] = position

        visit()
        visited.add(tile_num)

        # now i do this for all the neighbors
        neighbors = get_neighbors(tile_num, tiles, edge_key, reverse_edge)
        for neighbor_num in neighbors:
            if neighbor_num not in visited:
                dfs(neighbor_num, tile_num)

    dfs(list(tiles.keys())[0])
    return img


def get_img_boundaries(img):
    '''get the boundaries of img'''
    x_coords = sorted([idx[0] for idx in list(img.keys())])
    y_coords = sorted([idx[1] for idx in list(img.keys())])
    min_x, max_x = x_coords[0], x_coords[-1]
    min_y, max_y = y_coords[0], y_coords[-1]
    return (min_x, min_y), (max_x, max_y)


def print_img(img):
    '''print out the state of the img'''
    (min_x, min_y), (max_x, max_y) = get_img_boundaries(img)
    # need to add 10 to account for the length of the tile...
    for y_incr in range(max_y, min_y-1, -1):
        line = []
        for x_incr in range(min_x, max_x+1):
            if (x_incr, y_incr) not in img:
                line.append('.')
            else:
                line.append(img[(x_incr, y_incr)])
        print(''.join(line))


def remove_borders(img, tile_len):
    '''remove the borders....'''
    new_img = []
    (min_x, min_y), (max_x, max_y) = get_img_boundaries(img)
    for y_incr in range(max_y, min_y-1, -1):
        row = []
        for x_incr in range(min_x, max_x+1):
            if x_incr % tile_len == 0 or y_incr % tile_len == 0:
                continue
            if (x_incr+1) % tile_len == 0 or (y_incr-1) % tile_len == 0:
                continue
            row.append(img[(x_incr, y_incr)])
        if row:
            new_img.append(row)
    return new_img


def get_seamonster():
    '''return the seamonster as an array of arrays (# -> 1, blank ->0)'''
    seamonster = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """

    seamonster = seamonster.replace(' ', '0').replace('#', '1')
    seamonster = seamonster.split('\n')[1:]
    final = []
    for part in seamonster:
        row = []
        for value in list(part):
            row.append(value)
        final.append(row)
    return final


def count_monsters(img):
    '''count # seamonsters in img'''
    monster = get_seamonster()
    num_monster_cols = len(monster[0])
    num_img_cols = len(img[0])
    num_monsters = 0
    for row in range(len(img)-len(monster)):
        for start_col in range(0, num_img_cols-num_monster_cols):
            is_monster = True
            for monster_row, _ in enumerate(monster):
                for monster_col in range(num_monster_cols):
                    if monster[monster_row][monster_col] == '1'\
                         and img[row+monster_row][start_col+monster_col] != '1':
                        is_monster = False
            if is_monster:
                num_monsters += 1
    return num_monsters


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''find the # that aren't part of the sea monster....'''
    tiles = read_file(input_file)
    edge_key, reverse_edge = get_edge_keys(tiles)
    img = build_image(tiles, edge_key, reverse_edge)
    new_img = remove_borders(img, len(tiles[list(tiles.keys())[0]]))
    monster = get_seamonster()  # get the monster array

    # now for a given orientation, go thru and see whether i can find the monster...
    num_monsters = 0
    img_orientations = get_orientations(new_img)
    for orientation in img_orientations:
        monsters = count_monsters(orientation)
        if monsters > num_monsters:
            num_monsters = monsters

    num_dots = 0
    for row in new_img:
        num_dots += sum([int(char) for char in row])

    num_monster_dots = 0
    for row in monster:
        num_monster_dots += sum([int(char) for char in row])

    return num_dots - num_monsters*num_monster_dots
