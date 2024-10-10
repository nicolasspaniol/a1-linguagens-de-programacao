import unittest
from inflation import inflation_adj
from datetime import datetime
import math


# Só para facilitar a criação dos `datetime`s
def dt(year: int, month: int):
    return datetime(year, month, 10)


# Por pura semântica
any_dt = dt(2020, 1)
any_value = 100


class TestInflationAdj(unittest.TestCase):

    def test_date_in_future_should_raise_ValueError(self):
        with self.assertRaises(ValueError):
            inflation_adj(any_value, dt(2024, 10))

        with self.assertRaises(ValueError):
            inflation_adj(any_value, dt(2026, 7))

    def test_date_before_1997_should_raise_ValueError(self):
        with self.assertRaises(ValueError):
            inflation_adj(any_value, dt(1996, 12))

        with self.assertRaises(ValueError):
            inflation_adj(any_value, dt(1900, 8))

    def test_first_and_last_valid_dates_should_work(self):
        try:
            inflation_adj(any_value, datetime(1997, 1, 1))
            inflation_adj(any_value, datetime(2024, 9, 30))
        except ValueError:
            self.fail()

    def test_negative_value_should_raise_ValueError(self):
        with self.assertRaises(ValueError):
            inflation_adj(-1, any_dt)

        with self.assertRaises(ValueError):
            inflation_adj(float("-inf"), any_dt)

    def test_infinite_value_should_ramain_infinite(self):
        self.assertEqual(inflation_adj(float("inf"), any_dt), float("inf"))

    def test_value_zero_should_remain_zero(self):
        self.assertEqual(inflation_adj(0, any_dt), 0)

    def test_value_nan_should_raise_ValueError(self):
        with self.assertRaises(ValueError):
            inflation_adj(float("nan"), any_dt)

    def test_correct_inputs_should_match_expected(self):
        today = inflation_adj(100, dt(2020, 1))
        self.assertAlmostEqual(today, 120, delta=1)

        today = inflation_adj(200, dt(2015, 7))
        self.assertAlmostEqual(today, 252, delta=1)

        today = inflation_adj(10, dt(2000, 7))
        self.assertAlmostEqual(today, 17, delta=1)

        today = inflation_adj(1, dt(2000, 7))
        self.assertAlmostEqual(today, 1.7, delta=.1)

        today = inflation_adj(1000, dt(2024, 9))
        self.assertEqual(today, 1000)
        

if __name__ == "__main__":
    unittest.main()

