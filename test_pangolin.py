import numpy as np
import OpenGL.GL as gl
import pangolin

pangolin.CreateWindowAndBind('Main', 640, 480)
gl.glEnable(gl.GL_DEPTH_TEST)

# Define Projection and initial ModelView matrix
scam = pangolin.OpenGlRenderState(
    pangolin.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.2, 100),
    pangolin.ModelViewLookAt(-1, 1, -1, 0, 0, 0, pangolin.AxisDirection.AxisY))
handler = pangolin.Handler3D(scam)

# Create Interactive View in window
dcam = pangolin.CreateDisplay()
dcam.SetBounds(0.0, 1.0, 0.0, 1.0, -640.0/480.0)
dcam.SetHandler(handler)

# a = np.load("trymax.npy")
# xpos = np.array([float(x[1]) for x in a if x[0] == "xpos"])
# ypos = np.array([float(x[1]) for x in a if x[0] == "ypos"])
# zpos = np.array([float(x[1]) for x in a if x[0] == "zpos"])

# xpos = (xpos - xpos.min()) / (xpos.max() - xpos.min())
# ypos = (ypos - ypos.min()) / (ypos.max() - ypos.min())
# zpos = (zpos - zpos.min()) / (zpos.max() - zpos.min())

# pts_max = np.asarray(list(zip(xpos, zpos, ypos)))

# a = np.load("left_traj.npy")
# xposa = np.array([float(x[1]) for x in a if x[0] == "xpos"])
# yposa = np.array([float(x[1]) for x in a if x[0] == "ypos"])
# zposa = np.array([float(x[1]) for x in a if x[0] == "zpos"])

# xposa = (xposa - xpos.min()) / (xpos.max() - xpos.min())
# yposa = (yposa - ypos.min()) / (ypos.max() - ypos.min())
# zposa = (zposa - zpos.min()) / (zpos.max() - zpos.min())

# pts_left = np.asarray(list(zip(xposa, zposa, yposa)))

XMIN, XMAX = -27077.66796875, 22791.869140625
YMIN, YMAX = 496.66680908203125, 4287.50537109375
ZMIN, ZMAX = -14364.5126953125, 54478.3515625

a = np.load("centerline_traj.npy")
xposa = np.array([float(x[1]) for x in a if x[0] == "xpos"])
yposa = np.array([float(x[1]) for x in a if x[0] == "ypos"])
zposa = np.array([float(x[1]) for x in a if x[0] == "zpos"])

xposa = (xposa - XMIN) / (XMAX - XMIN)
yposa = (yposa - YMIN) / (YMAX - YMIN)
zposa = (zposa - ZMIN) / (ZMAX - ZMIN)

pts_center = np.asarray(list(zip(xposa, yposa, zposa)))


a = np.load("left_traj.npy")
xposa = np.array([float(x[1]) for x in a if x[0] == "xpos"])
yposa = np.array([float(x[1]) for x in a if x[0] == "ypos"])
zposa = np.array([float(x[1]) for x in a if x[0] == "zpos"])

xposa = (xposa - XMIN) / (XMAX - XMIN)
yposa = (yposa - YMIN) / (YMAX - YMIN)
zposa = (zposa - ZMIN) / (ZMAX - ZMIN)

pts_left = np.asarray(list(zip(xposa, yposa, zposa)))


while not pangolin.ShouldQuit():
    # # update this from thread?
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glClearColor(0.0, 0.0, 0.0, 1.0)
    dcam.Activate(scam)

    gl.glPointSize(2)
    gl.glColor3f(0.0, 0.0, 1.0)
    pangolin.DrawPoints(pts_center)

    gl.glPointSize(2)
    gl.glColor3f(1.0, 0.0, 0.0)
    pangolin.DrawPoints(pts_left)



    pangolin.FinishFrame()


