import lasagne.layers as L
import lasagne.nonlinearities as NL

from garage.core import Serializable
from garage.misc.overrides import overrides
from garage.policies import StochasticPolicy
from garage.theano.core import ConvNetwork
from garage.theano.core import LasagnePowered
from garage.theano.distributions import Categorical
from garage.theano.misc import tensor_utils
from garage.theano.spaces import Discrete


class CategoricalConvPolicy(StochasticPolicy, LasagnePowered):
    def __init__(
            self,
            name,
            env_spec,
            conv_filters,
            conv_filter_sizes,
            conv_strides,
            conv_pads,
            hidden_sizes=[],
            hidden_nonlinearity=NL.rectify,
            output_nonlinearity=NL.softmax,
            prob_network=None,
    ):
        """
        :param env_spec: A spec for the mdp.
        :param hidden_sizes: list of sizes for the fully connected
        hidden layers
        :param hidden_nonlinearity: nonlinearity used for each hidden
        layer
        :param prob_network: manually specified network for this
        policy, other network params are ignored
        :return:
        """
        assert isinstance(env_spec.action_space, Discrete)

        Serializable.quick_init(self, locals())

        self._env_spec = env_spec

        if prob_network is None:
            prob_network = ConvNetwork(
                input_shape=env_spec.observation_space.shape,
                output_dim=env_spec.action_space.n,
                conv_filters=conv_filters,
                conv_filter_sizes=conv_filter_sizes,
                conv_strides=conv_strides,
                conv_pads=conv_pads,
                hidden_sizes=hidden_sizes,
                hidden_nonlinearity=hidden_nonlinearity,
                output_nonlinearity=NL.softmax,
                name="prob_network",
            )

        self._l_prob = prob_network.output_layer
        self._l_obs = prob_network.input_layer
        self._f_prob = tensor_utils.compile_function(
            [prob_network.input_layer.input_var],
            L.get_output(prob_network.output_layer))

        self._dist = Categorical(env_spec.action_space.n)

        super(CategoricalConvPolicy, self).__init__(env_spec)
        LasagnePowered.__init__(self, [prob_network.output_layer])

    @property
    def vectorized(self):
        return True

    @overrides
    def dist_info_sym(self, obs_var, state_info_vars=None):
        return dict(prob=L.get_output(self._l_prob, {self._l_obs: obs_var}))

    @overrides
    def dist_info(self, obs, state_infos=None):
        return dict(prob=self._f_prob(obs))

    # The return value is a pair. The first item is a matrix (N, A), where each
    # entry corresponds to the action value taken. The second item is a vector
    # of length N, where each entry is the density value for that action, under
    # the current policy
    @overrides
    def get_action(self, observation):
        flat_obs = self.observation_space.flatten(observation)
        prob = self._f_prob([flat_obs])[0]
        action = self.action_space.weighted_sample(prob)
        return action, dict(prob=prob)

    def get_actions(self, observations):
        flat_obs = self.observation_space.flatten_n(observations)
        probs = self._f_prob(flat_obs)
        actions = list(map(self.action_space.weighted_sample, probs))
        return actions, dict(prob=probs)

    @property
    def distribution(self):
        return self._dist
