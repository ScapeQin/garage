import pickle
import unittest

from garage.theano.spaces.box import Box


class TestBox(unittest.TestCase):

    def test_pickleable(self):
        obj = Box(*args, **kwargs)
        round_trip = pickle.loads(pickle.dumps(obj))
        assert round_trip
