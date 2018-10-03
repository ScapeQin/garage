import unittest

from dm_control.suite import ALL_TASKS

from tests.fixtures import DmParameterizedTestCase, DmTestCase

suite = unittest.TestSuite()
for task in ALL_TASKS:
    suite.addTest(DmParameterizedTestCase.parametrize(DmTestCase, param=task))
unittest.TextTestRunner(verbosity=2).run(suite)
