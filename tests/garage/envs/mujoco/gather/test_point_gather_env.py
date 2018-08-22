import pickle
import unittest

from garage.envs.mujoco.gather.point_gather_env import PointGatherEnv


class TestPointGatherEnv(unittest.TestCase):

    def test_pickleable(self):
        env = PointGatherEnv(n_apples=1)
        round_trip = pickle.loads(pickle.dumps(env))
        assert round_trip
        assert round_trip.n_apples == env.n_apples
        step_env(round_trip)

    test_pickleable.broken = True
