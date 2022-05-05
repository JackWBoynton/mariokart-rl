import pickle, joblib
import os
import numpy as np


DOLPHIN_CONF_DIR = os.environ.get("DOLPHIN_CONF_DIR")
DOLPHIN_DIR = os.environ.get("DOLPHIN_DIR")
MK_ISO = os.environ.get("MK_ISO")

MEMORY_LOCATIONS = os.path.join(DOLPHIN_CONF_DIR, "MemoryWatcher/Locations.txt")
CONTROLLER_CONTROL_PATH = os.path.join(DOLPHIN_CONF_DIR, "Pipes/p3")
CONTROLLER_HOTKEY_PATH = os.path.join(DOLPHIN_CONF_DIR, "Pipes/p4")


XMIN, XMAX = -27077.66796875, 22791.869140625
YMIN, YMAX = 496.66680908203125, 4287.50537109375
ZMIN, ZMAX = -14364.5126953125, 54478.3515625

OUT_NP_STATE_NAMES = [
    "minutes",
    "seconds",
    "thirdseconds",
    "xpos",
    "ypos",
    "zpos",
    "prev_xpos",
    "prev_ypos",
    "prev_zpos",
    "current_lap",
    "max_lap",
    "item",
    "steer",
    "acceleration",
    "state_flags",
    "max_lap_completion",
    "current_lap_completion",
]
OUT_NP_STATE_NAMES_MAP = {y: x for x, y in enumerate(OUT_NP_STATE_NAMES)}

LOAD_STATE_DELAY = 3  # seconds to reload state
BUTTON_KEYDOWN_DELAY = 0.3  # keydown duration
MAX_RACETIME = 5  # 5 minutes max
MIN_VELOCITY = 0.5
LAP_REWARD_SCALE = 100
STATE_LOOKBACK = 10  # look at 10 previous states per step

TRAJ_CMAP = {
    "left": (1.0, 0.0, 0.0),
    "right": (0.0, 1.0, 0.0),
    "center": (0.0, 1.0, 1.0),
    "pos": (0.0, 0.0, 1.0),
}

from mario_env.envs.trajectory import Trajectory

try:
    print("loading track trajectories...") 
    CENTER_TRAJ = Trajectory(name="center", env=np.load(os.environ.get("CENTER_TRAJ")), writeable=False)
    RIGHT_TRAJ = Trajectory(name="right", env=np.load(os.environ.get("RIGHT_TRAJ")), writeable=False)
    LEFT_TRAJ = Trajectory(name="left", env=np.load(os.environ.get("LEFT_TRAJ")), writeable=False)
    print("loaded track trajectories")
except Exception as e:
    print(e)
    CENTER_TRAJ = None
    LEFT_TRAJ = None
    RIGHT_TRAJ = None

