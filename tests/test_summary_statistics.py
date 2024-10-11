import unittest
import pandas as pd
import numpy as np
from summary_statistics import chi2, contingency_coeff, cramer_v


# https://stackoverflow.com/a/32752318
def any_df(m: int, n: int) -> pd.DataFrame:
    return pd.DataFrame(
        np.random.randint(0, m, size=(m, n)),
        columns=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")[:n]
    )


any_m = 10
any_n = 10


class TestContingencyCoeff(unittest.TestCase):

    def test_two_rows_should_work(self):
        try:
            contingency_coeff(any_df(2, any_n))
        except ValueError:
            self.fail()

    def test_two_columns_should_work(self):
        try:
            contingency_coeff(any_df(any_m, 2))
        except ValueError:
            self.fail()

    def test_less_than_two_rows_should_raise_ValueError(self):
        with self.assertRaises(ValueError):
            contingency_coeff(any_df(1, any_n))
        
    def test_less_than_two_columns_should_raise_ValueError(self):
        with self.assertRaises(ValueError):
            contingency_coeff(any_df(any_m, 1))

    def test_not_numeric_data_should_raise_ValueError(self):
        data = np.random.rand(4, 3)
        string_column = ["A", "B", "C", "D"]
        df = pd.DataFrame(data, columns=["A", "B", "C"])
        df["D"] = string_column
     
        with self.assertRaises(ValueError):
            contingency_coeff(df)

        data = np.random.rand(4, 3)
        string_column = [True, False, False, False]
        df = pd.DataFrame(data, columns=["A", "B", "C"])
        df["D"] = string_column
     
        with self.assertRaises(ValueError):
            contingency_coeff(df)

    def test_result_should_be_positive(self):
        for i in range(100):
            df = any_df(any_m, any_n)
            self.assertGreaterEqual(contingency_coeff(df), 0)

    def test_no_association_should_yield_zero(self):
        df = pd.DataFrame()
        df["A"] = np.array([0, 1, 2, 3])
        df["B"] = np.array([0, 3, 6, 9])
        df["C"] = np.array([0, 0, 0, 0])
        self.assertEqual(contingency_coeff(df), 0)

    def test_correct_inputs_should_match_expected(self):
        df = pd.DataFrame([
            {"consumidor": 214, "produtor": 237, "escola": 78, "outras": 119},
            {"consumidor": 51, "produtor": 102, "escola": 126, "outras": 22},
            {"consumidor": 111, "produtor": 304, "escola": 139, "outras": 48}
        ])
        self.assertAlmostEqual(contingency_coeff(df), 0.3, delta=.1)


class TestChi2(unittest.TestCase):

    def test_two_rows_should_work(self):
        try:
            chi2(any_df(2, any_n))
        except ValueError:
            self.fail()

    def test_two_columns_should_work(self):
        try:
            chi2(any_df(any_m, 2))
        except ValueError:
            self.fail()

    def test_less_than_two_rows_should_raise_ValueError(self):
        with self.assertRaises(ValueError):
            chi2(any_df(1, any_n))
        
    def test_less_than_two_columns_should_raise_ValueError(self):
        with self.assertRaises(ValueError):
            chi2(any_df(any_m, 1))

    def test_not_numeric_data_should_raise_ValueError(self):
        data = np.random.rand(4, 3)
        string_column = ["A", "B", "C", "D"]
        df = pd.DataFrame(data, columns=["A", "B", "C"])
        df["D"] = string_column
     
        with self.assertRaises(ValueError):
            chi2(df)

        data = np.random.rand(4, 3)
        string_column = [True, False, False, False]
        df = pd.DataFrame(data, columns=["A", "B", "C"])
        df["D"] = string_column
     
        with self.assertRaises(ValueError):
            chi2(df)

    def test_result_should_be_positive(self):
        for i in range(100):
            df = any_df(any_m, any_n)
            self.assertGreaterEqual(chi2(df), 0)

    def test_no_association_should_yield_zero(self):
        df = pd.DataFrame()
        df["A"] = np.array([0, 1, 2, 3])
        df["B"] = np.array([0, 3, 6, 9])
        df["C"] = np.array([0, 0, 0, 0])
        self.assertEqual(chi2(df), 0)

    def test_correct_inputs_should_match_expected(self):
        df = pd.DataFrame([
            {"consumidor": 214, "produtor": 237, "escola": 78, "outras": 119},
            {"consumidor": 51, "produtor": 102, "escola": 126, "outras": 22},
            {"consumidor": 111, "produtor": 304, "escola": 139, "outras": 48}
        ])
        self.assertAlmostEqual(chi2(df), 173, delta=1)


class TestCramerV(unittest.TestCase):

    def test_two_rows_should_work(self):
        try:
            cramer_v(any_df(2, any_n))
        except ValueError:
            self.fail()

    def test_two_columns_should_work(self):
        try:
            cramer_v(any_df(any_m, 2))
        except ValueError:
            self.fail()

    def test_less_than_two_rows_should_raise_ValueError(self):
        with self.assertRaises(ValueError):
            cramer_v(any_df(1, any_n))
        
    def test_less_than_two_columns_should_raise_ValueError(self):
        with self.assertRaises(ValueError):
            cramer_v(any_df(any_m, 1))

    def test_not_numeric_data_should_raise_ValueError(self):
        data = np.random.rand(4, 3)
        string_column = ["A", "B", "C", "D"]
        df = pd.DataFrame(data, columns=["A", "B", "C"])
        df["D"] = string_column
     
        with self.assertRaises(ValueError):
            cramer_v(df)

        data = np.random.rand(4, 3)
        string_column = [True, False, False, False]
        df = pd.DataFrame(data, columns=["A", "B", "C"])
        df["D"] = string_column
     
        with self.assertRaises(ValueError):
            cramer_v(df)

    def test_result_should_be_between_zero_and_one(self):
        for i in range(10):
            df = any_df(any_m, any_n)
            v = cramer_v(df)
            self.assertGreaterEqual(v, 0)
            self.assertLessEqual(v, 1)

    def test_no_association_should_yield_zero(self):
        df = pd.DataFrame()
        df["A"] = np.array([0, 1, 2, 3])
        df["B"] = np.array([0, 3, 6, 9])
        df["C"] = np.array([0, 0, 0, 0])
        self.assertEqual(cramer_v(df), 0)

    def test_correct_inputs_should_match_expected(self):
        df = pd.DataFrame([
            {"consumidor": 214, "produtor": 237, "escola": 78, "outras": 119},
            {"consumidor": 51, "produtor": 102, "escola": 126, "outras": 22},
            {"consumidor": 111, "produtor": 304, "escola": 139, "outras": 48}
        ])
        self.assertAlmostEqual(cramer_v(df), 0.2, delta=.1)


if __name__ == "__main__":
    unittest.main()
