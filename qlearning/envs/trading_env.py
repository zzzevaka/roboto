import logging
import enum
import gym
from gym import spaces
from gym.utils import seeding


class MarketOrderTypes(enum.Enum):
    SELL = 0
    BUY = 1


class MarketOrder(object):
    def __init__(self,
                 order_type,
                 unit_count,
                 values,
                 close_diff_threshold=0.01,
                 max_steps=10,
                 tax=0):
        self.order_type = order_type
        self.unit_count = unit_count
        self.values = values
        self.open_value = values[0]
        self.down_threshold = self.open_value - self.open_value*close_diff_threshold
        self.up_threshold = self.open_value + self.open_value * close_diff_threshold
        self.max_steps = max_steps
        self.tax = tax

    def _calc_profit(self, new_value):
        tax = -(self.open_value * self.unit_count * self.tax)

        if self.order_type == MarketOrderTypes.SELL:
            profit = self.open_value - float(new_value)
        else:
            profit = float(new_value) - self.open_value
        return tax + round(profit, 5) * self.unit_count

    def take_profit(self):
        step = 0
        for value in self.values[1:]:
            step += 1
            should_close = False

            if step >= self.max_steps:
                should_close = True

            if not self.down_threshold < value < self.up_threshold:
                should_close = True

            if should_close:
                return self._calc_profit(value)
        return 0


class TradingEnv(gym.Env):

    def __init__(self, observ_data, target_data, order_close_threshold=0.01, order_tax=0):
        self.observation_history = observ_data
        self.target_history = target_data
        self.n_step = self.observation_history.shape[0] - 1
        self.observation_space = spaces.MultiDiscrete(self.observation_history)

        self.curr_step = None

        self.order_close_threshold = order_close_threshold
        self.order_tax = order_tax
        self.opened_market_order = None

        # 3 actions:
        #   - hold
        #   - sell
        #   - buy
        self.action_space = spaces.Discrete(3)

        self.wallet_amount = None

        # seed and start
        self._seed()
        self._reset()

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)

    def _reset(self):
        self.wallet_amount = 200
        self.curr_step = 0
        return self.current_observation

    def _step(self, action):
        assert self.action_space.contains(action)
        reward = self._calc_reward(action)
        self.curr_step += 1
        logging.debug(
            f'step: {self.curr_step}, reward: {reward}, amount: {self.wallet_amount}'
        )
        if self.curr_step == self.n_step or self.wallet_amount <= 0:
            done = True
        else:
            done = False
        info = {}
        return self.current_observation, reward, done, info

    def _calc_reward(self, action):
        if action == 0:
            return 0

        elif action == 1:
            order_type = MarketOrderTypes.SELL
        else:
            order_type = MarketOrderTypes.BUY

        unit_count = int(self.wallet_amount * 0.10)

        profit = MarketOrder(
            order_type=order_type,
            unit_count=int(self.wallet_amount * 0.10),
            values=self.target_history[self.curr_step:],
            close_diff_threshold=self.order_close_threshold,
            tax=self.order_tax,
        ).take_profit()

        self.wallet_amount += profit

        if self.wallet_amount <= 0:
            logging.info('wallet empy')
            return -2000

        return profit / unit_count

    @property
    def current_target_value(self):
        return self.target_history[self.curr_step]

    @property
    def current_observation(self):
        return self.observation_history[self.curr_step]

    def reset(self):
        return self._reset()

    def step(self, action):
        return self._step(action)
