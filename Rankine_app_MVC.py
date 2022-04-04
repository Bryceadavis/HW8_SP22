import sys
from PyQt5 import QtWidgets as qtw
from Rankine_GUI import Ui_Form
from Rankine_Classes import rankineController
from Calc_state import SatPropsIsobar
from Calc_state import UnitConverter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MainWindow(qtw.QWidget, Ui_Form):
    def __init__(self):
        """
        MainWindow constructor
        """
        super().__init__()
        # Main UI code goes here
        self.setupUi(self)
        self.AssignSlots()
        self.MakeCanvas()
        # A tuple containing the widgets that get updated in the View
        self.widgets = (self.le_H1, self.le_H2, self.le_H3, self.le_H4,
                        self.le_TurbineWork, self.le_PumpWork, self.le_HeatAdded,
                        self.le_Efficiency, self.lbl_SatPropHigh,
                        self.lbl_SatPropLow, self.ax, self.canvas)
        # A tuple containing the other widgets that get updated in the View
        self.otherwidgets = (self.le_PHigh, self.le_PLow, self.le_TurbineInletCondition,
                             self.lbl_PHigh, self.lbl_PLow, self.lbl_H1Units,
                             self.lbl_H2Units, self.lbl_H3Units, self.lbl_H4Units,
                             self.lbl_TurbineWorkUnits, self.lbl_PumpWorkUnits, self.lbl_HeatAddedUnits)
        self.RC = rankineController(self.widgets)  # instantiate a rankineController object

        # a place to store coordinates from last position on graph
        self.oldXData = 0.0
        self.oldYData = 0.0
        # End main ui code
        self.show()

    def AssignSlots(self):
        """
        Setup signals and slots for my program
        :return:
        """
        self.btn_Calculate.clicked.connect(self.Calculate)
        self.rdo_Quality.clicked.connect(self.SelectQualityOrTHigh)
        self.rdo_THigh.clicked.connect(self.SelectQualityOrTHigh)
        self.rb_SI.toggled.connect(self.SetUnits)
        self.rb_SI.toggled.connect(self.SelectQualityOrTHigh)
        self.btn_Calculate.clicked.connect(self.SetUnits)
        # for the below line edits, the changes made to them will not come into effect unless the user clicks 'enter'
        # Could not identify a way to get this to work without enter
        # If adjustments to pressures are not reasonable program may crash
        self.le_PHigh.returnPressed.connect(self.SelectQualityOrTHigh)  # user must press enter to proceed with results
        self.le_PHigh.returnPressed.connect(self.Calculate)  # must press enter
        self.le_PLow.returnPressed.connect(self.SetUnits)  # must press enter
        self.le_PLow.returnPressed.connect(self.Calculate)  # must press enter
        self.le_PHigh.returnPressed.connect(self.SetUnits)  # must press enter

    def MakeCanvas(self):
        """
        Create a place to make graph of Rankine cycle
        Step 1:  create a Figure object called self. Figure
        Step 2:  create a FigureCanvasQTAgg object called self. Canvas
        Step 3:  create an axes object for making plot
        Step 4:  add self. Canvas to self.gb_Output.layout() which is a grid layout
        :return:
        """
        # Step 1.
        self.figure = Figure(figsize=(2, 4), tight_layout=True, frameon=True)
        # Step 2.
        self.canvas = FigureCanvasQTAgg(self.figure)
        # Step 3.
        self.ax = self.figure.add_subplot()
        # Step 4.
        self.widgetsVerticalLayout.addWidget(self.canvas)
        self.canvas.mpl_connect("motion_notify_event", self.mouseMoveEvent)

    # since my main window is a widget, I can customize its events by overriding the default event
    def mouseMoveEvent(self, event):
        self.oldXData = event.xdata if event.xdata is not None else self.oldXData
        self.oldYData = event.ydata if event.ydata is not None else self.oldYData
        self.setWindowTitle('s:{:0.2f} kJ/(kg*K), T:{:0.2f} C'.format(self.oldXData, self.oldYData))

    def Calculate(self):
        """
        The first step needed is to define the two pressure iso-bars.
        Next this function will check the conditions of the form and proceed with the proper conversions.
        Lastly this function will utilize Update model from Rankine Controller to start the overall program. Went with
        Nested for loops in order to avoid crashes that occurred when the statements were broken out into separate
        functions
        :return:
        """
        PHigh = self.le_PHigh.text()  # defining high pressure to be equal to le text
        PLow = self.le_PLow.text()  # defining low pressure to be equal to le text
        # Had to use these nested if statements in this form. If these statements are separated into their own
        # functions as before it will cause the unit conversions to crash.
        if self.rb_SI.isChecked():  # if the radio button for SI is checked, Pressure will be converted to kpa
            PHigh = float(PHigh) * 100  # bar to kpa.
            PLow = float(PLow) * 100  # bart to kpa
            # if the radio button for Thigh is checked, text in the Turbine Inlet Condition line edit becomes input
            if self.rdo_THigh.isChecked():
                TurbineInletCondition = float(self.le_TurbineInletCondition.text())
            self.RC.updateModel((PHigh, PLow, self.rdo_Quality,
                                 self.le_TurbineInletCondition, self.le_TurbineEff), SI=True)

        if self.rb_English.isChecked():  # If radio Button English then pressures are converted to English Units
            PHigh = float(PHigh) * UnitConverter.bar_to_psi  # converting Bar to PSI
            PLow = float(PLow) * UnitConverter.bar_to_psi  # converting Bar to PSI

            if self.rdo_THigh.isChecked():  # Thigh is checked necessary conversion to use in RC.Rankine Model.
                TurbineInletCondition = float(self.le_TurbineInletCondition.text())
                TurbineInletCondition = UnitConverter.F_to_C(TurbineInletCondition)
                self.RC.updateModel((PHigh, PLow, self.rdo_Quality,
                                     TurbineInletCondition, self.le_TurbineEff), SI=False)

    def SelectQualityOrTHigh(self):
        """
        This function needs to consider Unit selection and then set both the text and default values for Thigh.
        Default Values for Thigh will be the default Tsat values for both English and SI Units.
        :return:
        """
        # Defining the Thigh label if SI Units
        if self.rb_SI.isChecked():
            self.lbl_TurbineInletCondition.setText(
                ("Turbine Inlet: {} =".format('x' if self.rdo_Quality.isChecked() else 'THigh (deg C)')))
        # Defining the Thigh label if english Units
        if self.rb_English.isChecked():
            self.lbl_TurbineInletCondition.setText(
                ("Turbine Inlet: {} =".format('x' if self.rdo_Quality.isChecked() else 'THigh (deg F)')))
        # Default Value will equal TSat if SI
        # Once again, had to collect the various functions and put them in this nested form in order to keep the
        # program from crashing
        if self.rb_SI.isChecked():
            T_HighNew = SatPropsIsobar(float(self.le_PHigh.text()) * 100).TSat
            if self.RC.Model.t_high is not None:  # found a way to denote if T_high has a value, this way the model
                # will update accordingly
                T_HighNew = self.RC.Model.t_high
            T_HighNew = "{:0.2f}".format(T_HighNew)
            # default value for line edit else the new temperature value will be used.
            self.le_TurbineInletCondition.setText(("1" if self.rdo_Quality.isChecked() else T_HighNew))
            if self.rb_English.isChecked():

                T_HighNew = SatPropsIsobar(float(self.le_PHigh.text()) / UnitConverter.kpa_to_psi).TSat  # converting
                if self.RC.Model.t_high is not None:
                    T_HighNew = self.RC.Model.t_high
                T_HighNew = round(UnitConverter.C_to_F(T_HighNew), 2)

                self.le_TurbineInletCondition.setText((flaot(self.rdo_Quality.text()) if self.rdo_Quality.isChecked()
                                                       else T_HighNew))

    def SetUnits(self):
        self.RC.updateUnits(self.widgets, self.otherwidgets, SI=self.rb_SI.isChecked())


# if this module is being imported, this won't run. If it is the main module, it will run.
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.setWindowTitle('Rankine calculator')
    mw.btn_Calculate.click()
    sys.exit(app.exec())
