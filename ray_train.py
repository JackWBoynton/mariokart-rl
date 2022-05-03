from ray.rllib.agents.ppo import PPOTrainer
from ray.rllib.agents.ddpg import DDPGTrainer
from ray.rllib.agents.dqn.apex import ApexTrainer


import mario_env

import ray
from ray import tune



ray.init()
tune.run(
    "SAC",
    config={
        "env": mario_env.envs.marioenv.MarioEnv,
        "num_gpus": 0,
        "num_workers": 1,
    },
)
