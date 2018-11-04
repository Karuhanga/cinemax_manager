from unittest import TestCase

from utils import *


class CinemaTests(TestCase):
    def test_load_seat_costs(self):
        costs = {
            Economy: 20000,
            VIP: 50000,
            VVIP: 100000,
            Twin: 25000
        }
        self.assertEqual(costs, load_seat_costs())

    def test_get_seat_cost(self):
        seat_costs = get_all_seat_costs()
        # economy
        self.assertEqual(seat_costs[Economy], get_seat_cost(row=M, column=1))
        self.assertEqual(seat_costs[Economy], get_seat_cost(row=O, column=1))
        self.assertEqual(seat_costs[Economy], get_seat_cost(row=P, column=14))

        # vip
        self.assertEqual(seat_costs[VIP], get_seat_cost(row=G, column=1))
        self.assertEqual(seat_costs[VIP], get_seat_cost(row=H, column=1))
        self.assertEqual(seat_costs[VIP], get_seat_cost(row=I, column=14))

        # vvip
        self.assertEqual(seat_costs[VVIP], get_seat_cost(row=C, column=1))
        self.assertEqual(seat_costs[VVIP], get_seat_cost(row=A, column=1))
        self.assertEqual(seat_costs[VVIP], get_seat_cost(row=A, column=20))

        # twin
        self.assertEqual(seat_costs[Twin], get_seat_cost(row=A, column=5))
        self.assertEqual(seat_costs[Twin], get_seat_cost(row=B, column=10))
        self.assertEqual(seat_costs[Twin], get_seat_cost(row=B, column=13))

    def test_seat_is_valid(self):
        # valid
        self.assertTrue(seat_is_valid('a1'))
        self.assertTrue(seat_is_valid('A1'))
        self.assertTrue(seat_is_valid('P7'))
        self.assertTrue(seat_is_valid('e20'))

        # not valid
        self.assertFalse(seat_is_valid('a21'))
        self.assertFalse(seat_is_valid('a40'))
        self.assertFalse(seat_is_valid('Q21'))
        self.assertFalse(seat_is_valid('z2'))
        self.assertFalse(seat_is_valid('a0'))
