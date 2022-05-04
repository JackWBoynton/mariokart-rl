import numpy as np
from .constants import *


class Trajectory:
    def __init__(self, name, x=[], y=[], z=[], writeable=True):
        assert name in TRAJ_CMAP.keys(), f"name: {name} not in TRAJ_CMAP"
        self.name = name
        self.xs, self.ys, self.zs = [], [], []
        self.writeable = writeable

        if len(x):
            assert (
                len(x) == len(y) == len(z)
                and sum([min(x), min(y), min(z)]) >= 0
                and sum([max(x), max(y), max(z)]) <= 3
            ), "x, y, z must be normalized and the same length"
            self.xs, self.ys, self.zs = x, y, z

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
    def is_bounded(self, trajx, trajy):
        current_pos = self.xs[-1], self.ys[-1], self.zs[-1]

        # 2D (x, y, z) -> (x, z)
        x, z = current_pos[0], current_pos[2]

        # horizontal line L
        

        