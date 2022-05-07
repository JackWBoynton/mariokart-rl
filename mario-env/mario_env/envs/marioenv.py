import gym
from gym import spaces
import numpy as np
import subprocess
import time
import queue
import math
import joblib
import threading
from shapely.geometry import Point

from .threaded_mw import MemoryWatcherThread
from .pad import Pad, Button, Stick
from .memory_watcher import MemoryWatcher
from .state_manager import StateManager
from .state import State
from .trajectory import Trajectory
from .constants import *
from .pangolin_handler import Visualizer, DDVisualizer

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="(%(threadName)-9s) %(message)s",
)


class DolphinController:
    def __init__(self, dolphin_dir=DOLPHIN_DIR):
        self.dolphin_dir = dolphin_dir
        self.dolphin_process = None

        self.memory_watcher_thread = MemoryWatcherThread()
        self.connect()
        self.memory_watcher_thread.start()

    def write_memory_locations(self):
        path = MEMORY_LOCATIONS
        with open(path, "w") as f:
            f.write("\n".join(self.memory_watcher_thread.state_manager.locations()))

    def connect(self):
        if self.dolphin_process == None:
            self.write_memory_locations()
            self.dolphin_process = subprocess.Popen(
                [self.dolphin_dir, "-e", MK_ISO]
            )  # , stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            time.sleep(3)

    def step(self):
        comb_states = np.zeros((17, STATE_LOOKBACK + 1))
        pstates = self.memory_watcher_thread.previous_states[
            -STATE_LOOKBACK:
        ]  # retrieve 10 previous most recent states
        cstate = self.memory_watcher_thread.state
        comb_states[:, 0] = cstate.asnumpy()  # 0 -> current state
        p = np.array([x.asnumpy() for x in pstates]).T
        comb_states[:, 1 : p.shape[-1] + 1] = p
        return comb_states

    def get_xyz_traj(self):
        trajxyz = self.memory_watcher_thread.state_manager.get_xyz_traj()
        x, y, z = (
            [x[1] for x in trajxyz if x[0] == "xpos"],
            [x[1] for x in trajxyz if x[0] == "ypos"],
            [x[1] for x in trajxyz if x[0] == "zpos"],
        )
        return np.asarray(x), np.asarray(y), np.asarray(z)

    def kill(self):
        if self.dolphin_process is not None:
            self.dolphin_process.kill()


class Controller:
    def __init__(
        self, pipe_loc=CONTROLLER_CONTROL_PATH, hotkey_loc=CONTROLLER_HOTKEY_PATH
    ):
        self.pad = Pad(pipe_loc)
        self.pad = self.pad.__enter__()
        self.reset_pad = Pad(hotkey_loc)
        self.reset_pad.__enter__()

    def tap(self, button_ind):
        assert button_ind <= 11, "Invalid Button action: " + str(button_ind)
        if button_ind in [5, 4, 3, 2]:
            return  # dont press start please
        self.pad.press_button(Button(button_ind))
        time.sleep(BUTTON_KEYDOWN_DELAY)
        self.pad.release_button(Button(button_ind))

    def stick(self, ind, x, y):

        self.pad.tilt_stick(Stick(ind), x, y)
        time.sleep(BUTTON_KEYDOWN_DELAY)
        self.pad.tilt_stick(Stick(ind), 0.5, 0.5)  # return to neutral position

    def reset(self):
        self.pad.reset()

    def send_action(self, act):
        # HANDLE BUTTON PRESSES
        buttons = act[:12]
        try:
            [self.tap(n) for n, x in enumerate(buttons) if x > 0.5]

            # HANDLE STICKS

            self.stick(0, act[13], act[14])
            self.stick(1, act[15], act[16])
        except BrokenPipeError:
            return True
        else:
            return False

    def load_state(self):  # returns should reset
        try:
            self.reset_pad.press_button(Button(13))
            time.sleep(BUTTON_KEYDOWN_DELAY)
            self.reset_pad.release_button(Button(13))
            time.sleep(LOAD_STATE_DELAY)
        except BrokenPipeError:
            return True
        else:
            return False


class MarioEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(
        self, config={"visualization": 1, "expert": {"on": 1, "filename": "./test.npy"}}
    ) -> None:
        super().__init__()
        self.dolphin = None
        self.controller = None

        self.vis = None
        self.vis_queue = None

        self.current_traj = Trajectory(name="pos")

        if config["visualization"] == 1:
            self.ddvis = DDVisualizer()
            # self.vis = Visualizer()

            # self.vis.paint([LEFT_TRAJ, RIGHT_TRAJ, CENTER_TRAJ])
            self.ddvis.paint([LEFT_TRAJ, RIGHT_TRAJ])

        self.action_space = spaces.Box(low=0.0, high=1.0, dtype=np.float32, shape=(17,))
        self.observation_space = spaces.Box(
            low=-0.01, high=1.01, dtype=np.float32, shape=(17, STATE_LOOKBACK + 1)
        )  #
        self.n = 0
        self.lap_times = [MAX_RACETIME] * 3

        self.config = config

    def bad_buttons_reward(self, action):
        out_rew = 0
        return out_rew

    def update_current_traj(self, state):
        self.current_traj.update(
            state[OUT_NP_STATE_NAMES_MAP["xpos"]],
            state[OUT_NP_STATE_NAMES_MAP["ypos"]],
            state[OUT_NP_STATE_NAMES_MAP["zpos"]],
        )

    def step(self, action):

        self.n += 1
        should_reset = False
        if self.config["expert"]["on"] != 1:
            should_reset = self.controller.send_action(action)
        # print(f"sent action: {action}")
        new_state = self.dolphin.step()

        all_states = new_state
        pstates = new_state[:, 1:]
        new_state = new_state[:, 0]

        self.update_current_traj(new_state)  # update curr_traj
        curr_point = Point(new_state[OUT_NP_STATE_NAMES_MAP["xpos"]], new_state[OUT_NP_STATE_NAMES_MAP["zpos"]])
        if self.vis:
            self.vis.paint(
                [self.current_traj, LEFT_TRAJ, RIGHT_TRAJ, CENTER_TRAJ]
            )  # update current_traj on plot
            self.ddvis.paint(curr_point)
        

        # print(Trajectory.on_road(self.current_traj.numpy_pts()[-1], LEFT_TRAJ, RIGHT_TRAJ))

        if new_state is not None:
            if (
                new_state[OUT_NP_STATE_NAMES_MAP["current_lap_completion"]] >= 1
                and new_state[OUT_NP_STATE_NAMES_MAP["current_lap_completion"]] < 2
            ):
                self.lap_times[
                    int(new_state[OUT_NP_STATE_NAMES_MAP["current_lap_completion"]])
                ] = (time.time() - self.lap_dt)
                self.lap_dt = time.time()
            elif (
                new_state[OUT_NP_STATE_NAMES_MAP["current_lap_completion"]] >= 2
                and new_state[OUT_NP_STATE_NAMES_MAP["current_lap_completion"]] < 3
            ):
                self.lap_times[
                    int(new_state[OUT_NP_STATE_NAMES_MAP["current_lap_completion"]])
                ] = (time.time() - self.lap_dt)
                self.lap_dt = time.time()
            elif (
                new_state[OUT_NP_STATE_NAMES_MAP["current_lap_completion"]] >= 3
                and new_state[OUT_NP_STATE_NAMES_MAP["current_lap_completion"]] < 4
            ):
                self.lap_times[
                    int(new_state[OUT_NP_STATE_NAMES_MAP["current_lap_completion"]])
                ] = (time.time() - self.lap_dt)
                self.lap_dt = time.time()

            reward = self.calculate_reward(new_state)

            done = self.isdone(new_state)

            if should_reset:
                done = True
                self.dolphin = None
                self.controller = None
                self.reset()

            # all_states[all_states <= 0] = 1.

            return (
                np.nan_to_num(all_states, nan=0.0).astype(np.float32),
                reward,
                False if self.config["expert"]["on"] == 1 else done,
                {},
            )
        return self.observation_space.sample(), 0, False, {}

    def save_traj(self):
        self.dolphin.memory_watcher_thread.state_manager.serialize2write(
            self.config["expert"]["filename"]
        )

    def vbetween(self, pt1, pt2):
        x, y, z = pt1
        xx, yy, zz = pt2
        return (xx - x), (yy - y), (zz - z)

    def dist_between(self, pt1, pt2):
        dx, dy, dz = self.vbetween(pt1, pt2)
        return math.sqrt(dx**2 + dy**2 + dz**2)

    def dirr(self, trajx, trajy, trajz, trajxx, trajyy, trajzz, dd=1):
        """return the trajectory dot product of trajx, trajy, trajz @ trajxx, trajyy, trajzz

        Args:
            trajx (_type_): _description_
            trajy (_type_): _description_
            trajz (_type_): _description_
            trajxx (_type_): _description_
            trajyy (_type_): _description_
            trajzz (_type_): _description_
            dd (int, optional): _description_. Defaults to 1.

        Returns:
            _type_: _description_
        """
        out = 0
        trajx, trajy, trajz = (
            trajx[: len(trajxx)],
            trajy[: len(trajxx)],
            trajz[: len(trajxx)],
        )

        for (p, pp), (s, ss) in zip(
            list(
                zip(
                    list(zip(trajxx[0::dd], trajyy[0::dd], trajzz[0::dd])),
                    list(zip(trajxx[dd::dd], trajyy[dd::dd], trajzz[dd::dd])),
                )
            ),
            list(
                zip(
                    list(zip(trajx[0::dd], trajy[0::dd], trajz[0::dd])),
                    list(zip(trajx[dd::dd], trajy[dd::dd], trajz[dd::dd])),
                )
            ),
        ):
            v_curr = (pp[0] - p[0], pp[1] - p[1], pp[2] - p[2])
            v_expe = (ss[0] - s[0], ss[1] - s[1], ss[2] - s[2])
            out += np.array(v_curr) @ np.array(v_expe)
        return out

    def calculate_reward(self, new_state):

        lap_rewards = [
            abs(min((lt - MAX_RACETIME) / MAX_RACETIME, 0) * LAP_REWARD_SCALE)
            for lt in self.lap_times
        ]

        speed = self.vec3_speed(new_state)

        path_following_loss = Trajectory.get_path_loss((new_state[OUT_NP_STATE_NAMES_MAP["zpos"]], new_state[OUT_NP_STATE_NAMES_MAP["xpos"]]), (new_state[OUT_NP_STATE_NAMES_MAP["prev_zpos"]], new_state[OUT_NP_STATE_NAMES_MAP["prev_xpos"]]))

        return (speed + sum(lap_rewards)) - path_following_loss

    def vec3_speed(self, state):
        """find the speed of kart at a given state

        Args:
            state (np.ndarray): State object representated as a numpy array

        Returns:
            float: velocity of the kart given State state
        """
        x, y, z = (
            state[OUT_NP_STATE_NAMES_MAP["xpos"]],
            state[OUT_NP_STATE_NAMES_MAP["ypos"]],
            state[OUT_NP_STATE_NAMES_MAP["zpos"]],
        )
        x_, y_, z_ = (
            state[OUT_NP_STATE_NAMES_MAP["prev_xpos"]],
            state[OUT_NP_STATE_NAMES_MAP["prev_ypos"]],
            state[OUT_NP_STATE_NAMES_MAP["prev_zpos"]],
        )
        return math.sqrt(abs(x - x_) ** 2 + abs(y - y_) ** 2 + abs(z - z_) ** 2)

    def isdone(self, state):
        on_road = Trajectory.on_road(point=curr_point, ltraj=LEFT_TRAJ, rtraj=RIGHT_TRAJ) # bool
        if not on_road:
            return True

        if (
            state[OUT_NP_STATE_NAMES_MAP["max_lap_completion"]]
            > state[OUT_NP_STATE_NAMES_MAP["current_lap_completion"]]
        ):  # is not as far as was before lol
            return True
        if state[OUT_NP_STATE_NAMES_MAP["minutes"]] is None:
            return False
        x = self.vec3_speed(state)
        if x > 0 and x < MIN_VELOCITY:
            return True
        return False

    def reset(self):
        print("called reset")
        self.lap_dt = time.time()
        self.n = 0

        if self.dolphin is None:
            self.dolphin = DolphinController()
            time.sleep(5)
        if self.controller is None:
            self.controller = Controller()
            time.sleep(5)

        print("sent reload state")
        should_hardrst = (
            self.controller.load_state()
        )  # reload state to start of the race
        if should_hardrst:
            self.dolphin = None
            self.controller = None
            self.reset()

        [self.controller.tap(0) for _ in range(5)]  # send kick
        return self.observation_space.sample()
