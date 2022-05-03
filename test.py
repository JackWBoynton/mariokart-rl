
import gym
import mario_env

env_id = "MarioEnv-v0"

env = gym.make(env_id)
env.reset()
try:
    while 1:
        env.step([0] * 17)
except KeyboardInterrupt:
    print("saving")
    env.save_traj()

