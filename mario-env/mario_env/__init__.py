from gym.envs.registration import register
from .envs import MarioEnv
from .envs.trajectory import Trajectory
from .envs.pangolin_handler import Visualizer
from .envs import constants as Constants
register(
    id='MarioEnv-v0',
    entry_point='mario_env.envs:MarioEnv',
)

