from stable_baselines import DQN
from stable_baselines.gail import generate_expert_traj

from mario_env import MarioEnv

model = DQN('MlpPolicy', 'MarioEnv-v1', verbose=1)
      # Train a DQN agent for 1e5 timesteps and generate 10 trajectories
      # data will be saved in a numpy archive named `expert_cartpole.npz`
generate_expert_traj(model, 'expert_cartpole', n_timesteps=int(1e5), n_episodes=10)