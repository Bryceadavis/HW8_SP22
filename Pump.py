import sys

import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from Pump_GUI import Ui_Form
#from Pump_Classes import PumpController
import Calc_state
from Calc_state import SatPropsIsobar
from Calc_state import UnitConverter as UC
from Rankine_Classes import rankineView
# test
# test test test test test test testy hello!!!!
#these imports are necessary for drawing a matplot lib graph on my GUI
#no simple widget for this exists in QT Designer, so I have to add the widget in code.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

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

    def OpenDialog(self):  #borrowed from Dr.Smay's PipeNetwork_App
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
        data_list=[]
        # for x in data[3:]:
        #     gbs=str.split(data[x],"  ")
        #     data_list.append(gbs)
        #     pass
        nums=data[3:]
        apple=[]
        for x in nums:
            banana=str.strip(x,'\n')
            oranges=str.split(banana,"  ")
            apple.append(oranges)
        peaches=np.array(apple)
        flow=peaches[:,0]
        head=peaches[:,1]
        efficiency=peaches[:,2]

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
        self.figure=Figure(figsize=(2,4),tight_layout=True, frameon=True)
        #Step 2.
        self.canvas=FigureCanvasQTAgg(self.figure)
        #Step 3.
        self.ax = self.figure.add_subplot()
        #Step 4.
        # self.Output_groupBox.layout().addWidget(self.canvas, 6)
        # self.canvas.mpl_connect("motion_notify_event", self.mouseMoveEvent)

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