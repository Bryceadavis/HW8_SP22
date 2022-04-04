import sys

import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from Pump_GUI2 import Ui_Form
#from Pump_Classes import PumpController
import Calc_state
from Calc_state import SatPropsIsobar
from Calc_state import UnitConverter as UC
from Rankine_Classes import rankineView

from Calc_state import Steam_SI as steam
from Calc_state import SatPropsIsobar
from matplotlib import pyplot as plt
# test
# test test test test test test testy hello!!!! #test
#these imports are necessary for drawing a matplot lib graph on my GUI
#no simple widget for this exists in QT Designer, so I have to add the widget in code.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
#some code borrowed from Rankine_app_MVC also
class MainWindow(qtw.QWidget, Ui_Form):
    def __init__(self):
        """
        MainWindow constructor
        """
        super().__init__()  #if you inherit, you generally should run the parent constructor first.
        # Main UI code goes here
        self.setupUi(self)
        self.AssignSlots()
        self.MakeCanvas()
        #A tuple containing the widgets that get updated in the View
        # self.widgets = (self.lineEdit_2, self.lineEdit_3, self.lineEdit_4, self.lineEdit_5, self.lineEdit_6, self.ax, self.canvas)
        # self.RC = PumpController(self.widgets)  # instantiate a rankineController object
        # a place to store coordinates from last position on graph
        #self.otherwidgets = (self.le_PHigh, self.le_PLow, self.le_TurbineInletCondition, self.lbl_PHigh, self.lbl_PLow, self.lbl_H1Units, self.lbl_H2Units, self.lbl_H3Units, self.lbl_H4Units, self.lbl_TurbineWorkUnits, self.lbl_PumpWorkUnits, self.lbl_HeatAddedUnits)
        self.oldXData=0.0
        self.oldYData=0.0
        # End main ui code
        self.show()

    def AssignSlots(self):
        """
        Setup signals and slots for my program
        :return:
        """
        self.ExitPushButton.clicked.connect(self.ExitApp)
        self.FilenamePushButton.clicked.connect(self.OpenDialog)
        # self.rdo_THigh.clicked.connect(self.SelectQualityOrTHigh)
        # self.le_PLow.textChanged[str].connect(self.NewPlow)
        # self.le_PHigh.textChanged[str].connect(self.NewPhigh)
        # self.le_TurbineInletCondition.textChanged[str].connect(self.NewT)
        # self.rb_English.clicked.connect(self.SetUnits)

    def OpenDialog(self):  # some code borrowed from Dr.Smay's PipeNetwork_App
        """
        Read the information from a pipe network file.
        :return:
        """
        # open the file dialog box to search for the file I want
        filename = qtw.QFileDialog.getOpenFileName()[0]
        if len(filename) == 0:  # no file selected
            return
        self.le_Filename.setText(filename)  # echo the filename on the GUI
        file = open(filename, 'r')  # open the file
        data = file.readlines()  # read all the lines of the file into a list of strings
        file.close()
        # self.Controller.importPipeNetwork(data, PN=self.Model)  # import the pipe network information
        # self.updateView()  # update the view of the model
        self.le_Filename.setText(filename)
        self.lineEdit_2.setText(data[0])
        Flow_and_Head=str.split(data[2],"    ")
        self.lineEdit_3.setText(Flow_and_Head[0])
        #Head_Units=str.partition(Flow_and_Head[5]," ")
        self.lineEdit_6.setText(Flow_and_Head[1])
        # data_list=[]
        # for x in data[3:]:
        #     gbs=str.split(data[x],"  ")
        #     data_list.append(gbs)
        #     pass
        nums=data[3:]
        ap=[]
        for x3 in nums:
            ban=str.strip(x3,'\n')
            ora=str.split(ban,"  ")
            ap.append(ora)
        #pch=np.array(ap)
        flow=[]
        head=[]
        efficiency=[]
        for x2 in ap:
            flow.append(float(x2[0]))
        for y2 in ap:
            head.append(float(y2[1]))
        for z in ap:
            efficiency.append(float(z[2]))
        flow2=np.array(flow)
        head2=np.array(head)
        efficiency2=np.array(efficiency)
        #print(flow2)
        curve_head=np.polyfit(flow,head,3)
        # curve_head_str=str.strip(str(curve_head[0]), " ")
        curve_efficiency=np.polyfit(flow,efficiency,3)
        self.lineEdit_4.setText("{:.4f}, {:.4f}, {:.4f}, {:.4f}".format(curve_head[3],curve_head[2],curve_head[1],curve_head[0]))
        self.lineEdit_5.setText("{:.4f}, {:.4f}, {:.4f}, {:.4f}".format(curve_efficiency[3], curve_efficiency[2], curve_efficiency[1], curve_efficiency[0]))
        # poly1D_fn=np.poly1d(curve_head)
        cv_hd_ln= lambda x: curve_head[0]*(x**3)+curve_head[1]*(x**2)+curve_head[2]*(x)+curve_head[3]
        cv_eff_ln= lambda y: curve_efficiency[0]*(y**3)+curve_efficiency[1]*(y**2)+curve_efficiency[2]*(y)+curve_efficiency[3]
        xp = np.linspace(15, 43, 100)
        ax1 = self.ax
        ax1.clear()
        ax1.plot(xp, cv_hd_ln(xp), '--', color='k')
        ax1.plot(flow,head,'o', markerfacecolor='w', markeredgecolor='k')
        ax1.set_ylim(5, 75)
        ax1.set_ylabel('Head (ft)')
        ax1.set_xlabel('Flow Rate (gpm)')
        ax1.legend(['Head($R^2$ = 1.000)', 'Head'], loc=6)
        # Work done on second axis
        ax2 = ax1.twinx()
        ax2.set_ylabel('Efficiency (%)')
        ax2.plot(xp, cv_eff_ln(xp), ':', color='k')
        ax2.plot(flow, efficiency, '^', markerfacecolor='w', markeredgecolor='k')
        #ax2.plot(flow2, efficiency2, marker='^', markeredgecolor='k', markerfacecolor='w')
        ax2.set_ylim(5, 59)
        ax2.legend(['Efficiency($R^2$=.989)', 'Efficiency'], loc=1)
        self.canvas.draw()


        pass

    def Plot_doub(self):

        pass

    def ExitApp(self):
            app.exit()

    def MakeCanvas(self):
        """
        Create a place to make graph of Rankine cycle
        Step 1:  create a Figure object called self.figure
        Step 2:  create a FigureCanvasQTAgg object called self.canvas
        Step 3:  create an axes object for making plot
        Step 4:  add self.canvas to self.gb_Output.layout() which is a grid layout
        :return:
        """
        #Step 1.
        self.figure=Figure(figsize=(2,4),frameon=True) #tight_layout=True cannot be used w/ vertical layout
        #Step 2.
        self.canvas=FigureCanvasQTAgg(self.figure)
        #Step 3.
        self.ax = self.figure.add_subplot()
        #Step 4.
        self.verticalLayout.addWidget(self.canvas)

        #self.plot_cycle_TS(self.ax,self.figure)
        #self.canvas.mpl_connect("motion_notify_event", self.mouseMoveEvent)

    # def plot_cycle_TS(self, axObj=None, Model=None):
    #     """
    #     I want to plot the Rankine cycle on T-S coordinates along with the vapor dome and shading in the cycle.
    #     I notice there are several lines on the plot:
    #     saturated liquid T(s) colored blue
    #     saturated vapor T(s) colored red
    #     The high and low isobars and lines connecting state 1 to 2, and 3 to saturated liquid at phigh
    #     step 1:  build data for saturated liquid line
    #     step 2:  build data for saturated vapor line
    #     step 3:  build data between state 3 and sat liquid at p_high
    #     step 4:  build data between sat liquid at p_high and state 1
    #     step 5:  build data between state 1 and state 2
    #     step 6:  build data between state 2 and state 3
    #     step 7:  put together data from 3,4,5 for top line and build bottom line
    #     step 8:  make and decorate plot
    #
    #     Note:  will plot using pyplot if axObj is None else just returns
    #
    #     :param axObj:  if None, used plt.subplot else a MatplotLib axes object.
    #     :return:
    #     """
    #     # step 1&2:
    #     ts, ps, hfs, hgs, sfs, sgs, vfs, vgs = np.loadtxt('sat_water_table.txt', skiprows=1,
    #                                                       unpack=True)  # use np.loadtxt to read the saturated properties
    #     ax = Figure.subplot() if axObj is None else axObj
    #
    #     ax.plot(sfs, ts, color='blue')
    #     ax.plot(sgs, ts, color='red')
    #
    #     # step 3:  I'll just make a straight line between state3 and state3p
    #     st3p = steam(Model.p_high, x=0)  # saturated liquid state at p_high
    #     svals = np.linspace(Model.state3.s, st3p.s, 20)
    #     tvals = np.linspace(Model.state3.T, st3p.T, 20)
    #     line3 = np.column_stack([svals, tvals])
    #     # plt.plot(line3[:,0], line3[:,1])
    #
    #     # step 4:
    #     sat_pHigh = steam(Model.p_high, x=1.0)
    #     st1 = Model.state1
    #     svals2p = np.linspace(st3p.s, sat_pHigh.s, 20)
    #     tvals2p = [st3p.T for i in range(20)]
    #     line4 = np.column_stack([svals2p, tvals2p])
    #     if st1.T > sat_pHigh.T:  # need to add data points to state1 for superheated
    #         svals_sh = np.linspace(sat_pHigh.s, st1.s, 20)
    #         tvals_sh = np.array([steam(Model.p_high, s=ss).T for ss in svals_sh])
    #         line4 = np.append(line4, np.column_stack([svals_sh, tvals_sh]), axis=0)
    #     # plt.plot(line4[:,0], line4[:,1])
    #
    #     # step 5:
    #     svals = np.linspace(Model.state1.s, Model.state2.s, 20)
    #     tvals = np.linspace(Model.state1.T, Model.state2.T, 20)
    #     line5 = np.array(svals)
    #     line5 = np.column_stack([line5, tvals])
    #     # plt.plot(line5[:,0], line5[:,1])
    #
    #     # step 6:
    #     svals = np.linspace(Model.state2.s, Model.state3.s, 20)
    #     tvals = np.array([Model.state2.T for i in range(20)])
    #     line6 = np.column_stack([svals, tvals])
    #     # plt.plot(line6[:,0], line6[:,1])
    #
    #     # step 7:
    #     topLine = np.append(line3, line4, axis=0)
    #     topLine = np.append(topLine, line5, axis=0)
    #     xvals = topLine[:, 0]
    #     y1 = topLine[:, 1]
    #     y2 = [Model.state3.T for s in xvals]
    #
    #     ax.plot(xvals, y1, color='darkgreen')
    #     ax.plot(xvals, y2, color='black')
    #     ax.fill_between(xvals, y1, y2, color='gray', alpha=0.5)
    #     ax.plot(Model.state1.s, Model.state1.T, marker='o', markeredgecolor='k', markerfacecolor='w')
    #     ax.plot(Model.state2.s, Model.state2.T, marker='o', markeredgecolor='k', markerfacecolor='w')
    #     ax.plot(Model.state3.s, Model.state3.T, marker='o', markeredgecolor='k', markerfacecolor='w')
    #     ax.set_xlabel(r's $\left(\frac{kJ}{kg\cdot K}\right)$', fontsize=18)  # different than plt
    #     ax.set_ylabel(r'T $\left( ^{o}C \right)$', fontsize=18)  # different than plt
    #     ax.set_title(Model.name)  # different than plt
    #     ax.grid(visible='both', alpha=0.5)
    #     ax.tick_params(axis='both', direction='in', labelsize=18)
    #
    #     sMin = min(sfs)
    #     sMax = max(sgs)
    #     ax.set_xlim(sMin, sMax)  # different than plt
    #
    #     tMin = min(ts)
    #     tMax = max(max(ts), st1.T)
    #     ax.set_ylim(tMin, tMax * 1.05)  # different than plt
    #
    #     txt = 'Summary:'
    #     txt += '\n$\eta_{cycle} = $' + '{:0.2f}%'.format(Model.efficiency)
    #     txt += '\n$\eta_{turbine} = $' + '{:0.2f}'.format(Model.turbine_eff)
    #     txt += '\n$W_{turbine} = $' + '{:0.2f}'.format(Model.turbine_work) + r'$\frac{kJ}{kg}$'
    #     txt += '\n$W_{pump} = $' + '{:0.2f}'.format(Model.pump_work) + r'$\frac{kJ}{kg}$'
    #     txt += '\n$Q_{in} = $' + '{:0.2f}'.format(Model.heat_added) + r'$\frac{kJ}{kg}$'
    #     ax.text(sMin + 0.05 * (sMax - sMin), tMax, txt, ha='left', va='top', fontsize=18)  # different than plt
    #
    #     if axObj is None:  # this allows me to show plot if not being displayed on a figure
    #         plt.show()

    #since my main window is a widget, I can customize its events by overriding the default event

    # def Calculate(self):
    #     #use rankineController to update the model based on user inputs
    #     self.RC.updateModel((self.le_PHigh, self.le_PLow, self.rdo_Quality, self.le_TurbineInletCondition, self.le_TurbineEff))


#if this module is being imported, this won't run. If it is the main module, it will run.
if __name__== '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.setWindowTitle('Pump Data')
    pass
    sys.exit(app.exec())
