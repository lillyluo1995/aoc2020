from typing import IO
import re
import numpy as np


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''what's the first bus i can take after the earliest time and how long
     will i have to wait for it?return the product of those two #s'''

    # parse in the info. we need the x's in p_2 but not p_1 so diffs
    earliest_time, buses = input_file.readlines()
    earliest_time = int(earliest_time)
    buses = [int(bus) for bus in re.findall('[0-9]+', buses)]
    buses.sort()

    # to find the first bus i take, i need to find the bus that minimizes bus-earliest time%bus
    min_mod = earliest_time+buses[-1]
    min_bus = 0
    for bus in buses:
        mod_time = bus-earliest_time % bus
        if mod_time < min_mod:
            min_mod = mod_time
            min_bus = bus
    return min_mod*min_bus


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''now i care about the x's. what's the first time stamp s.t. modulo is incrementing
    by 1?
    guess 1: 224028385328878 too low'''

    _, buses_str = input_file.readlines()
    buses_str = re.findall('x|[0-9]+', buses_str)
    req_mod = list(range(0, len(buses_str)))

    # basically i need find a number s.t. n%13=0, n%41 = 3, ...
    mapping = {int(bus): req_mod_ for bus, req_mod_ in zip(
        buses_str, req_mod) if bus != 'x'}
    buses = list(mapping.keys())

    # check bus #s coprime before using chinese remainder theorem
    assert np.gcd.reduce(buses) == 1

    crt_array = [np.prod([bus for bus in buses if bus != target])
                 for target in buses]
    for idx, bus in enumerate(buses):
        current = crt_array[idx]
        current_mod = current % bus
        req_remainder = (bus-mapping[bus]) % bus

        mult = 1
        while (current_mod * mult) % bus != req_remainder:
            mult += 1
        crt_array[idx] *= mult
    return sum(crt_array) % np.prod(buses)
