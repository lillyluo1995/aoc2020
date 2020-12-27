import aoc.d25

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part(25, False, aoc.d25.p_1)

    def test_part_two(self):
        self.run_aoc_part(25, False, aoc.d25.p_2)
