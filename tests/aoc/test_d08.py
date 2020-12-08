import aoc.d08

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    '''run test to see if it works'''
    def test_part_one(self):
        '''run test to see if it works'''
        self.run_aoc_part(8, False, aoc.d08.p_1)

    def test_part_two(self):
        '''run test to see if it works'''
        self.run_aoc_part(8, False, aoc.d08.p_2)
