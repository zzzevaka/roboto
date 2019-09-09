import unittest
import numpy as np
from qlearning.envs.trading_env import *


class MarketOrderTestCase(unittest.TestCase):

    def setUp(self):
        self.order = MarketOrder(
            order_type=MarketOrderTypes.SELL,
            unit_count=1,
            values=[10, 10.01, 9.9, 10.3, 10.5],
        )

    def test_take_profit(self):
        self.assertEqual(self.order.take_profit(), 0.1)

        self.order.values=[10, 10.1, 9.9, 10.3, 10.5]
        self.assertEqual(self.order.take_profit(), -0.1)

        self.order.values = [10, 10.01, 9.99, 10.3, 10.5]
        self.assertEqual(self.order.take_profit(), -0.3)

        self.order.values = [10, 10, 10, 10]
        self.assertEqual(self.order.take_profit(), 0)

        self.order.values = [10, 10, 10, 10]
        self.assertEqual(self.order.take_profit(), 0)

        self.order.order_type = MarketOrderTypes.BUY
        self.order.values = [10, 10.1, 9.99, 10.3, 10.5]
        self.assertEqual(self.order.take_profit(), 0.1)


class TradingEnvTestCase(unittest.TestCase):
    OBSERV_DATA = np.array([
        [10, 9, 4],
        [11, 8, 5],
        [10, 7, 2],
        [ 9, 9, 6],
        [10, 9, 4],
        [11, 8, 5],
        [10, 7, 2],
        [9, 9, 6],
        [10, 9, 4],
        [11, 8, 5],
        [10, 7, 2],
        [9, 9, 6],
    ])

    TARGET_DATA = np.array([5,3,2,1,5,3,2,1,5,3,2,1])

    def setUp(self):
        self.env = TradingEnv(
            self.OBSERV_DATA,
            self.TARGET_DATA
        )

    def test_reset(self):
        self.assertTrue((self.OBSERV_DATA[0] == self.env.reset()).all())

    def test_step_hold(self):
        next_state, reward, done, info = self.env.step(0)
        self.assertTrue((self.OBSERV_DATA[1] == next_state).all())
        self.assertEqual(reward, 0)
        self.assertFalse(done)

    def test_step_sell(self):
        next_state, reward, done, info = self.env.step(1)
        self.assertEqual(reward, 2.0)

    def test_step_buy(self):
        next_state, reward, done, info = self.env.step(2)
        self.assertEqual(reward, -2.0)

    def test_done(self):
        for i in range(len(self.OBSERV_DATA) - 2):
            self.env.step(0)
        next_state, reward, done, info = self.env.step(0)
        self.assertTrue((self.OBSERV_DATA[-1] == next_state).all())
        self.assertTrue(done)
