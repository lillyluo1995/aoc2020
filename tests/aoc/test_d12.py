import aoc.d12

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    '''run test to see if it works'''
    def test_part_one(self):
        '''run test to see if it works'''
        self.run_aoc_part(12, False, aoc.d12.p_1)

    def test_part_two(self):
        '''run test to see if it works'''
        self.run_aoc_part(12, False, aoc.d12.p_2)
