import numpy as np
from .constants import *


class Trajectory:
    def __init__(self, name, x=[], y=[], z=[], env=None, writeable=True):
        assert name in TRAJ_CMAP.keys(), f"name: {name} not in TRAJ_CMAP"
        self.name = name
        self.xs, self.ys, self.zs = [], [], []
        self.writeable = writeable

        if len(x) and env is None:
            assert len(x) == len(y) == len(z), "x, y, z must be the same length"
            if not (sum([min(x), min(y), min(z)]) >= 0 and sum([max(x), max(y), max(z)]) <= 3):
                x, y, z = Trajectory.norm(x, y, z)
            self.xs, self.ys, self.zs = x, y, z
        elif env is not None:
            self.xs, self.ys, self.zs = env

    def update(self, x, y, z):
        assert self.writeable, f"Trajectory {self.name} is not writable"
        if isinstance(x, list):
            assert (
                len(x) == len(y) == len(z)
                and sum([min(x), min(y), min(z)]) >= 0
                and sum([max(x), max(y), max(z)]) <= 3
            ), "x, y, z must be normalized and the same length"
            self.xs += x
            self.ys += y
            self.zs += z
        else:
            self.xs += [x]
            self.ys += [y]
            self.zs += [z]

    def get_pts_in_3d_box(self, box):
        bxmin, bxmax, bymin, bymax, bzmin, bzmax = box
        out = []

        for x, y, z in zip(self.xs, self.ys, self.zs):
            if (
                bxmin <= x <= bxmax and bymin <= y <= bymax and bzmin <= z <= bzmax
            ):  # pt is in box
                out.append((x, y, z))

        return out

    def __len__(self):
        return len(self.xs)

    def pangolin_pts(self):
        return self.xs, self.ys, self.zs

    @staticmethod
    def is_bounded(trajx, trajy, trajz):
        current_pos = self.xs[-1], self.ys[-1], self.zs[-1]

        # 2D (x, y, z) -> (x, z)
        x, z = current_pos[0], current_pos[2]

        # horizontal line L
    
    @staticmethod
    def norm(x=None, y=None, z=None, np_traj=None):
        if np_traj is not None:
            trajx = [float(x[-1]) for x in np_traj if x[0] == "xpos"]
            trajy = [float(x[-1]) for x in np_traj if x[0] == "ypos"]
            trajz = [float(x[-1]) for x in np_traj if x[0] == "zpos"]
        elif x is not None:
            trajx = x
            trajy = y
            trajz = z
        m = min([len(trajx), len(trajy), len(trajz)])
        trajx = (np.array(trajx[:m]) - XMIN) / (XMAX - XMIN)
        trajy = (np.array(trajy[:m]) - YMIN) / (YMAX - YMIN)
        trajz = (np.array(trajz[:m]) - ZMIN) / (ZMAX - ZMIN)

        return trajx, trajy, trajz
        

        