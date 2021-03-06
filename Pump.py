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
        #creating a code that will read the information from a pipe network file 
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
        self.le_Filename.setText(filename) #Name  the text to filename
        self.lineEdit_2.setText(data[0]) #Name the set Text to data
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
        flow=[] #defined the flow and calculating in list 
        head=[] #defined the head, and going to add in list 
        efficiency=[] #defined the efficiency
        for x2 in ap:
            flow.append(float(x2[0]))
        for y2 in ap:
            head.append(float(y2[1]))
        for z in ap:
            efficiency.append(float(z[2]))
        flow2=np.array(flow) #create an array for the flow
        head2=np.array(head) #create an array for the Head
        efficiency2=np.array(efficiency) #create an array that includes the efficiency
        #print(flow2)
        curve_head=np.polyfit(flow,head,3) #creat the polyfit for the flow and head into a curve head
        # curve_head_str=str.strip(str(curve_head[0]), " ") 
        curve_efficiency=np.polyfit(flow,efficiency,3) # create a polyfit for the flow and efficiency into a curve
        self.lineEdit_4.setText("{:.4f}, {:.4f}, {:.4f}, {:.4f}".format(curve_head[3],curve_head[2],curve_head[1],curve_head[0])) # formatting line edit 
        self.lineEdit_5.setText("{:.4f}, {:.4f}, {:.4f}, {:.4f}".format(curve_efficiency[3], curve_efficiency[2], curve_efficiency[1], curve_efficiency[0]))
        # poly1D_fn=np.poly1d(curve_head)
        cv_hd_ln= lambda x: curve_head[0]*(x**3)+curve_head[1]*(x**2)+curve_head[2]*(x)+curve_head[3]
        cv_eff_ln= lambda y: curve_efficiency[0]*(y**3)+curve_efficiency[1]*(y**2)+curve_efficiency[2]*(y)+curve_efficiency[3]
        xp = np.linspace(15, 43, 100)  # linspace to plug in values 
        ax1 = self.ax  # subplots
        ax1.clear() # subplots 
        ax1.plot(xp, cv_hd_ln(xp), '--', color='k')
        ax1.plot(flow,head,'o', markerfacecolor='w', markeredgecolor='k')
        ax1.set_ylim(5, 75)
        ax1.set_ylabel('Head (ft)')  # labels 
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


#if this module is being imported, this won't run. If it is the main module, it will run.
if __name__== '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.setWindowTitle('Pump Data')
    pass
    sys.exit(app.exec())
