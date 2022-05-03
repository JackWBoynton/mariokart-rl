import numpy as np
import OpenGL.GL as gl
import pangolin
import threading

from .constants import *

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class Visualizer(threading.Thread):
    def __init__(self, event, queue):
        super(Visualizer, self).__init__(name="visualizer")
        self.event = event
        self.queue = queue

        pangolin.CreateWindowAndBind('Trajectory Visualization', 640, 480)
        gl.glEnable(gl.GL_DEPTH_TEST)

        # Define Projection and initial ModelView matrix
        self.scam = pangolin.OpenGlRenderState(
            pangolin.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.2, 100),
            pangolin.ModelViewLookAt(-1, 1, -1, 0, 0, 0, pangolin.AxisDirection.AxisY))
        self.handler = pangolin.Handler3D(self.scam)

        # Create Interactive View in window
        self.dcam = pangolin.CreateDisplay()
        self.dcam.SetBounds(0.0, 1.0, 0.0, 1.0, -640.0/480.0)
        self.dcam.SetHandler(self.handler)

        self.points_list = {}

    def run(self):
        logging.debug(f'watching for traj updates and updating plot')
        event_set = self.event.wait()
        logging.debug(f'waiting for new data to plot...')
        while not pangolin.ShouldQuit():
            if event_set:
                self.event.clear() # reset event state to false 
                # add trajectories to plot
                while not self.queue.empty():
                    traj = self.queue.get()
                    xs, ys, zs = traj.pangolin_pts()
                    self.points_list[traj.name] = {"pts": [xs, ys, zs], "color": TRAJ_CMAP[traj.name] if TRAJ_CMAP[traj.name] else (1.0, 0.0, 0.0)}

            if len(list(self.points_list.keys())) > 0:
                # update plot
                gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
                gl.glClearColor(0.0, 0.0, 0.0, 1.0)
                self.dcam.Activate(self.scam)

                for traj_name in self.points_list.keys(): # need to redraw previous trajectories too
                    gl.glPointSize(2)
                    gl.glColor3f(self.points_list[traj_name]["color"])
                    pangolin.DrawPoints(self.points_list[traj_name]["pts"])
                
                pangolin.FinishFrame()