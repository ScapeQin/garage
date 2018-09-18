import pickle
import unittest

from garage.tf.spaces import Discrete
from garage.tf.spaces.product import Product


class TestProduct(unittest.TestCase):
    def test_pickleable(self):
        obj = Product([Discrete(3), Discrete(2)])
        round_trip = pickle.loads(pickle.dumps(obj))
        assert round_trip