from typing import IO
import copy


def read_file(input_file):
    '''read the input file'''
    return [list(x.replace('\n', '')) for x in input_file.readlines()]


def get_eligible_adj(coord_, max_):
    '''return one of [0,1], [-1,0], [-1,0,1] depending on the coord'''
    if coord_ == 0:
        eligible = [0, 1]
    elif coord_ == max_:
        eligible = [-1, 0]
    else:
        eligible = [-1, 0, 1]
    return eligible


def get_new_seat_contents(current_seat, num_occupied, tolerance):
    '''determine what the new seat will become based on the number of occupied seats around it'''
    new_seat = current_seat
    if current_seat == 'L':
        if num_occupied == 0:
            new_seat = '#'
    elif current_seat == '#':
        if num_occupied >= tolerance:
            new_seat = 'L'
    return new_seat


def calc_multiplier(seat_coord, max_, chg):
    '''calc how many times out we have to go'''
    out = [0, 0]  # x out, y out
    for dim in range(2):
        if chg[dim] < 0:
            out[dim] = seat_coord[dim]
        elif chg[dim] > 0:
            out[dim] = max_[dim] - seat_coord[dim]
        else:  # if 0 out
            out[dim] = ValueError
    return min(mult for mult in out if mult is not ValueError)


def get_new_seat(seats, seat_coord, max_, tolerance, vision=False):
    '''get what a given seat coord should become based on the rules'''
    x_eligible, y_eligible = get_eligible_adj(seat_coord[0], max_[0]), \
        get_eligible_adj(seat_coord[1], max_[1])
    num_occupied = 0
    for x_chg in x_eligible:
        for y_chg in y_eligible:
            if x_chg == 0 and y_chg == 0:
                continue
            if vision:
                multiplier = calc_multiplier(
                    seat_coord, max_, (x_chg, y_chg))
                for mult in range(1, multiplier+1):
                    seat_contents = seats[seat_coord[0]+mult*x_chg][seat_coord[1]+mult*y_chg]
                    if seat_contents == '#':
                        num_occupied += 1
                        break
                    if seat_contents == 'L':
                        break
            else:
                seat_contents = seats[seat_coord[0]+x_chg][seat_coord[1]+y_chg]
                if seat_contents == '#':
                    num_occupied += 1
    current_seat = seats[seat_coord[0]][seat_coord[1]]
    return get_new_seat_contents(current_seat, num_occupied, tolerance)


def count_seats(seats):
    '''count number of occupied seats'''
    num_occupied = 0
    for row in seats:
        for col in row:
            if col == '#':
                num_occupied += 1
    return num_occupied


def print_seats(seats):
    '''print out the seat map for ease of debugging'''
    for row in seats:
        print(''.join(row))


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''apply the seating algo and until the number of occupied seats are stable
    then return number of occupied seats'''
    seats = read_file(input_file)
    max_x = len(seats)-1
    max_y = len(seats[0])-1
    # x will denote the row (the first index in the array of arrays)
    # y will denote the col (the index within the array of an array)
    stable = False
    idx = 0
    tolerance = 4
    while not stable and idx < 2000:
        new_seats = copy.deepcopy(seats)
        for x_coord in range(max_x+1):
            for y_coord in range(max_y+1):
                new_seats[x_coord][y_coord] = get_new_seat(seats, (x_coord, y_coord),
                                                           (max_x, max_y), tolerance)
        if new_seats == seats:
            stable = True
        else:
            seats = copy.deepcopy(new_seats)
            idx += 1
    return count_seats(seats)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''now we care about all the seats within a passenger's range of vision
    #1: 337 too low'''
    seats = read_file(input_file)
    (max_x, max_y) = (len(seats)-1, len(seats[0])-1)

    # x will denote the row (the first index in the array of arrays)
    # y will denote the col (the index within the array of an array)
    stable = False
    idx = 0
    tolerance = 5
    while not stable and idx < 2000:
        new_seats = copy.deepcopy(seats)
        for x_coord in range(max_x+1):
            for y_coord in range(max_y+1):
                new_seats[x_coord][y_coord] = get_new_seat(seats, (x_coord, y_coord),
                                                           (max_x, max_y), tolerance, True)
        if new_seats == seats:
            stable = True
        else:
            seats = copy.deepcopy(new_seats)
            idx += 1
    return count_seats(seats)
