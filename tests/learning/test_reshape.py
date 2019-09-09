import numpy as np
import pandas as pd
from unittest import TestCase
from learning.preprocessing import reshape_with_window


class ReshaheTestCase(TestCase):

    def setUp(self):
        data = np.array([
            [1,2,3],
            [2,5,6],
            [3,8,9],
            [10,11,12],
            [13,14,15],
            [16,17,18],
        ])
        self.df = pd.DataFrame(
            columns=['t1', 't2', 't3'],
            data=data,
        )

    def test_reshape_with_window_2d(self):
        data_test = np.array([
            [1,2,3,2,5,6,3,8,9],
            [2,5,6,3,8,9,10,11,12],
            [3,8,9,10,11,12,13,14,15],
            [10,11,12,13,14,15,16,17,18],
        ])
        reshaped_data = reshape_with_window(self.df, [1,2], self.df.columns, False)

        self.assertTrue((reshaped_data == data_test).all())

    def test_reshape_with_window_3d(self):
        data_test = np.array([
            [
                [1,2,3],
                [2,5,6],
                [3,8,9],
            ],
            [
                [2,5,6],
                [3,8,9],
                [10,11,12],
            ],
            [
                [3,8,9],
                [10,11,12],
                [13,14,15],
            ],
            [
                [10,11,12],
                [13,14,15],
                [16,17,18],
            ],
        ])
        reshaped_data = reshape_with_window(self.df, [1,2], self.df.columns, True)
        self.assertTrue((reshaped_data == data_test).all())
