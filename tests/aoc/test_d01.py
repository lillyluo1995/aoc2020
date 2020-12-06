import aoc.d01

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    '''tests to see if it works'''
    def test_part_one(self):
        '''run test to see if it works'''
        self.run_aoc_part(1, False, aoc.d01.p_1)

    def test_part_two(self):
        '''run test to see if it works'''
        self.run_aoc_part(1, False, aoc.d01.p_2)
