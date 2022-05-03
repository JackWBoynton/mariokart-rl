from gym.envs.registration import register
from .envs import MarioEnv
register(
    id='MarioEnv-v0',
    entry_point='mario_env.envs:MarioEnv',
)

