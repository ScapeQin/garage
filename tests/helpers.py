import unittest

import tensorflow as tf

from tests.quirks import KNOWN_GYM_RENDER_NOT_IMPLEMENTED
from tests.quirks import KNOWN_GYM_CLOSE_BROKEN


class TfTest(unittest.TestCase):

    def setUp(self):
        self.sess = tf.Session()
        self.sess.__enter__()

    def tearDown(self):
        self.sess.__exit__(None, None, None)
        self.sess.close()


def step_env(env, n=10, render=True):
    env.reset()
    for _ in range(n):
        _, _, done, _ = env.step(env.action_space.sample())
        if render:
            env.render()
        if done:
            break
    env.close()


def step_env_with_gym_quirks(test_case, env, spec, n=10, render=True):
    env.reset()
    for _ in range(n):
        _, _, done, _ = env.step(env.action_space.sample())
        if render and not spec.id in KNOWN_GYM_RENDER_NOT_IMPLEMENTED:
            env.render()
        else:
            with test_case.assertRaises(NotImplementedError):
                env.render()
        if done:
            break
    if not spec.id in KNOWN_GYM_CLOSE_BROKEN:
        env.close()
    else:
        with test_case.assertRaisesRegex(
                AttributeError, "'MjViewer' object has no attribute 'finish'"):
            env.close()
