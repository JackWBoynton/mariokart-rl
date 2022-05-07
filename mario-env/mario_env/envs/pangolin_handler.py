import numpy as np
import OpenGL.GL as gl

import threading
import sys
import multiprocessing

from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
import shapely
from descartes import PolygonPatch

from .trajectory import Trajectory

import matplotlib
import matplotlib.pyplot as plt

from queue import LifoQueue
from multiprocessing.managers import BaseManager


# if sys.platform == "darwin": # macos multiprocessing fix
#     multiprocessing.set_start_method('spawn')

from multiprocessing import Process, Queue

from .constants import TRAJ_CMAP

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="(%(threadName)-9s) %(message)s",
)

class Visualizer(object):
    def __init__(self):
        import pangolin
        self.state = None
        self.q = Queue()
        self.vp = Process(target=self.viewer_thread, args=(self.q,))
        self.vp_daemon = True
        self.vp.start()

    def viewer_thread(self, q):
        self.viewer_init(1024, 768)
        while 1:
            self.viewer_refresh(q)

    def viewer_init(self, w, h):
        pangolin.CreateWindowAndBind("Trajectory Visualization", w, h)
        gl.glEnable(gl.GL_DEPTH_TEST)

        self.scam = pangolin.OpenGlRenderState(
            pangolin.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.2, 100),
            pangolin.ModelViewLookAt(-1, 1, -1, 0, 0, 0, pangolin.AxisDirection.AxisY),
        )
        self.handler = pangolin.Handler3D(self.scam)

        # Create Interactive View in window
        self.dcam = pangolin.CreateDisplay()
        self.dcam.SetBounds(0.0, 1.0, 0.0, 1.0, -640.0 / 480.0)
        self.dcam.SetHandler(self.handler)

    def viewer_refresh(self, q):
        while not q.empty():
            self.state = q.get()

            if self.state is not None:
                if isinstance(self.state, list):
                    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
                    gl.glClearColor(0.0, 0.0, 0.0, 1.0)
                    self.dcam.Activate(self.scam)
                    for traj in self.state:
                        xs, ys, zs = traj.pangolin_pts()
                        if len(xs) > 0:
                            gl.glPointSize(3) if traj.name == "pos" else gl.glPointSize(1)
                            gl.glColor3f(*TRAJ_CMAP[traj.name])
                            pts = np.asarray(list(zip(xs,  list([0] * len(ys)), zs)))
                            pangolin.DrawPoints(pts)

                pangolin.FinishFrame()
                # might add other stuff here i guess...

    def paint(self, trajs):
        self.q.put(trajs)


class MyManager(BaseManager):
    pass
MyManager.register('LifoQueue', LifoQueue)

class DDVisualizer(object):
    def __init__(self,):
        self.state = None
        # self.manager = MyManager()
        # self.manager.start()
        self.q = Queue(maxsize=1)
        self.vp = Process(target=self.viewer_thread, args=(self.q,))
        self.vp_daemon = True
        self.vp.start()
        

    def viewer_thread(self, q):
        self.curr_point = None
        self.past_point = None
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)


        while 1:
            self.viewer_refresh(q)

    def viewer_refresh(self, q):
        while not q.empty():
            self.state = q.get()

            if self.state is not None:
                if isinstance(self.state, matplotlib.patches.PathPatch):
                    self.ax.add_patch(self.state)
                else:
                    if self.curr_point:
                        self.curr_point.remove()      
                    self.past_point = self.state    
                    self.curr_point = self.ax.scatter(self.state.y, self.state.x, s=10000, color='gold',marker='+')
                # might add other stuff here i guess...
            plt.draw() 
            plt.pause(0.0000001) #is necessary for the plot to update for some reason

    def paint(self, trajs):
        if isinstance(trajs, list):
            if isinstance(trajs[0], Trajectory):
                xposa, yposa, zposa = trajs[0].pangolin_pts()
                polya=Polygon(list(zip(zposa, xposa))[:-200]) 
                xposa, yposa, zposa = trajs[1].pangolin_pts()
                polyb=Polygon(list(zip(zposa, xposa))[:-200])  
                poly_patch=PolygonPatch(polya - polyb)

                self.q.put(poly_patch)
        else:
            # print("traj inside pangolin_handler", trajs.x, trajs.y)
            self.q.put(trajs)
        