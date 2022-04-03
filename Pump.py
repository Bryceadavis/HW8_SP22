import numpy as np
from Calc_state import Steam_SI as steam  # import any of your own classes as you wish

import sys
#from PyQt5.QtWidgets import QWidget, QApplication
# from PyQt5.QtWidgets import QFileDialog, QMessageBox
# from PyQt5.QtGui import QCursor
# from PyQt5.QtCore import Qt

from Pump_GUI import Ui_Form  # from the GUI file your created

import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

class main_window(qtw.QWidget, Ui_Form):
    def __init__(self):
        """
        Constructor for the main window of the application.  This class inherits from QWidget and Ui_Form
        """
        super().__init__()  # run constructor of parent classes
        self.setupUi(self)  # run setupUi() (see Ui_Form)
        # $JES MISSING CODE$ ('Steam Property Calculator') # set the window title
        self.setWindowTitle( 'Pump Data') #&AKO

        self.assign_widgets()  # connects signals and slots
        self.show()

    def assign_widgets(self):
        """This function controls what happens when the GUI buttons are clicked."""
        self.ExitPushButton.clicked.connect(self.ExitApp) #closes app when exit is clicked
        # dialog= QFileDialog(self)
        # dialog.setFileMode(QFileDialog.AnyFile)
        self.FilenamePushButton.clicked.connect(self.OpenDialog) #calls Calculate function when Calculate is clicked

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
        # self.Controller.importPipeNetwork(data, PN=self.Model)  # import the pipe network information
        # self.updateView()  # update the view of the model
        pass

    def ExitApp(self):
        app.exit()

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = main_window()
    mw.setWindowTitle('Pipe Network Designer')
    sys.exit(app.exec())