import numpy as np
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
from descartes import PolygonPatch
from .constants import *

class Trajectory:
    def __init__(self, name, x=[], y=[], z=[], env=None, writeable=True):
        assert name in TRAJ_CMAP.keys(), f"name: {name} not in TRAJ_CMAP"
        self.name = name
        self.xs, self.ys, self.zs = [], [], []
        self.writeable = writeable

        if env is not None:
            
            x, y, z = Trajectory.check_norm(np_traj=env)
        
        if len(x):
            self.update(x, y, z, force=1)
            

    def update(self, x, y, z, force=0):
        if not force: assert self.writeable, f"Trajectory {self.name} is not writable"
        if isinstance(x, list) or isinstance(x, np.ndarray):
            assert len(x) == len(y) == len(z), "x, y, z must be the same length"
            self.xs = np.concatenate((self.xs, x))
            self.ys = np.concatenate((self.ys, y))
            self.zs = np.concatenate((self.zs, z))
            
        else:
            self.xs += [x]
            self.ys += [y]
            self.zs += [z]

        self.xs, self.ys, self.zs = Trajectory.check_norm(self.xs, self.ys, self.zs)
        
        return None

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
        return Trajectory.check_norm(self.xs, self.ys, self.zs)

    def numpy_pts(self):
        return np.array(list(zip(self.xs, self.ys, self.zs)))

    @staticmethod
    def is_bounded(trajx, trajy, trajz):
        current_pos = self.xs[-1], self.ys[-1], self.zs[-1]

        # 2D (x, y, z) -> (x, z)
        x, z = current_pos[0], current_pos[2]

        # horizontal line L
    
    @staticmethod
    def check_norm(x=None, y=None, z=None, np_traj=None):
        trajx = x
        trajy = y
        trajz = z

        if np_traj is not None:
            trajx = [float(x[-1]) for x in np_traj if x[0] == "xpos"]
            trajy = [float(x[-1]) for x in np_traj if x[0] == "ypos"]
            trajz = [float(x[-1]) for x in np_traj if x[0] == "zpos"]

        
        m = min([len(trajx), len(trajy), len(trajz)])
        if not (sum([min(trajx), min(trajy), min(trajz)]) >= 0 and sum([max(trajx), max(trajy), max(trajz)]) <= 3):

            trajx = (np.array(trajx[:m]) - XMIN) / (XMAX - XMIN)
            trajy = (np.array(trajy[:m]) - YMIN) / (YMAX - YMIN)
            trajz = (np.array(trajz[:m]) - ZMIN) / (ZMAX - ZMIN)

        return trajx, trajy, trajz
    
    @staticmethod
    def on_road(point, ltraj, rtraj):
        x, y, z = ltraj.pangolin_pts()
        a = Polygon(list(zip(z, x))[:-200])

        x, y, z = rtraj.pangolin_pts()
        b = Polygon(list(zip(z, x))[:-200])
        
        track = a - b
        return track.contains(Point(point.y, point.x))
        