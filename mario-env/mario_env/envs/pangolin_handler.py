import numpy as np
import OpenGL.GL as gl
import pangolin
import threading
from multiprocessing import Process, Queue

from .constants import *

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="(%(threadName)-9s) %(message)s",
)

class Visualizer(object):
    def __init__(self):
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
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            gl.glClearColor(0.0, 0.0, 0.0, 1.0)
            self.dcam.Activate(self.scam)

            if self.state is not None:
                for traj in self.state:
                    xs, ys, zs = traj.pangolin_pts()
                    if len(xs) > 0:
                        gl.glPointSize(3) if traj.name == "pos" else gl.glPointSize(1)
                        gl.glColor3f(*TRAJ_CMAP[traj.name])
                        pts = np.asarray(list(zip(xs, ys, zs)))
                        pangolin.DrawPoints(pts)

                pangolin.FinishFrame()

    def paint(self, trajs):
        self.q.put(trajs)
