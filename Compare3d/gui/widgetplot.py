from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import QTimer
from operator import attrgetter
import numpy as np
import math


class MyDynamicMplCanvas(FigureCanvas):

    def __init__(self, option,pose_error,pose_est,pose_real,map,id_markers,rpy_map,world,parent=None, width=6, height=4, dpi=100):

        self.fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


        self.map = map
        self.id_markers = id_markers
        self.world = world
        self.rpy_markers = rpy_map
        self.poseEst = pose_est
        self.poseReal = pose_real
        self.option = option
        self.pose_error = pose_error
        self.it = 0

        # Timer
        timer = QTimer(self)
        timer.timeout.connect(self.update_figure)
        self.dt = 250
        timer.start(self.dt)


    def calculate_arrow(self,origin,rpy,scale=0.2):
        x=origin[0]
        y=origin[1]
        dx=scale*math.cos(rpy[2])
        dy=scale*math.sin(rpy[2])
        return x,y,dx,dy

    def update_figure(self):


        if self.option == "showXYZ":
            self.fig.clf()
            self.axes = self.fig.add_subplot(111)
            self.axes.cla()

            xEst = list(map(attrgetter('x'), self.poseEst))
            yEst = list(map(attrgetter('y'), self.poseEst))

            xReal = list(map(attrgetter('x'), self.poseReal))
            yReal = list(map(attrgetter('y'), self.poseReal))

            xmap = list(map(attrgetter('x'), self.map))
            ymap = list(map(attrgetter('y'), self.map))


            if self.world:
                for x,y in self.world:
                    self.axes.plot(x, y, 'k')



            for i,xy in enumerate(zip(xmap, ymap)):
                id = self.id_markers[i]
                rpy = self.rpy_markers[i]
                self.axes.annotate('%d' % id, xy=xy, textcoords='data')
                x,y,dx,dy = self.calculate_arrow(xy,rpy)
                self.axes.arrow(x,y,dx,dy,width=0.005,color='k')


            # print(xEst,yEst)
            self.axes.plot(xEst, yEst,'.r',
                           xReal, yReal, '.b',xmap,ymap,'*k')
            self.axes.grid()
            self.draw()


        if self.option == "showRPY":
            ### Angle RPY
            self.fig.clf()
            self.axes = self.fig.add_subplot(311)
            PosRealR = list(map(attrgetter('roll'), self.poseReal))
            PosEstR = list(map(attrgetter('roll'), self.poseEst))
            t = np.linspace(0,len(PosEstR),len(PosEstR))
            self.axes.plot(t, PosRealR,'b', t, PosEstR,'r')

            self.axes = self.fig.add_subplot(312)
            PosRealY = list(map(attrgetter('yaw'), self.poseReal))
            PosEstY = list(map(attrgetter('yaw'), self.poseEst))
            self.axes.plot(t, PosRealY,'b', t, PosEstY,'r')

            self.axes = self.fig.add_subplot(313)
            PosRealP = list(map(attrgetter('pitch'), self.poseReal))
            PosEstP = list(map(attrgetter('pitch'), self.poseEst))
            self.axes.plot(t, PosRealP,'b', t, PosEstP,'r')

            self.draw()



        if self.option == "showErrorRPY":
            ### Angle RPY
            self.fig.clf()
            self.axes = self.fig.add_subplot(311)
            ErrorR = list(map(attrgetter('roll'), self.pose_error))
            t = np.linspace(0, len(ErrorR), len(ErrorR))
            self.axes.plot(t, ErrorR)

            self.axes = self.fig.add_subplot(312)
            ErrorY = list(map(attrgetter('yaw'), self.pose_error))
            self.axes.plot(t, ErrorY)

            self.axes = self.fig.add_subplot(313)
            ErrorP = list(map(attrgetter('pitch'), self.pose_error))

            self.axes.plot(t, ErrorP)
            self.draw()


        if self.option == "showErrorXYZ":
            ### Angle RPY
            self.fig.clf()
            self.axes = self.fig.add_subplot(311)
            ErrorX = list(map(attrgetter('x'), self.pose_error))
            t = np.linspace(0, len(ErrorX), len(ErrorX))
            self.axes.plot(t, ErrorX)

            self.axes = self.fig.add_subplot(312)
            Errory = list(map(attrgetter('y'), self.pose_error))
            self.axes.plot(t, Errory)

            self.axes = self.fig.add_subplot(313)
            ErrorZ = list(map(attrgetter('z'), self.pose_error))

            self.axes.plot(t, ErrorZ)
            self.draw()


    def setOption(self,option):
        self.option=option

