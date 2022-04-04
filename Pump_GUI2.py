# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Pump_GUI2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(990, 314)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gb_Input = QtWidgets.QGroupBox(Form)
        self.gb_Input.setObjectName("gb_Input")
        self.gridLayout = QtWidgets.QGridLayout(self.gb_Input)
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_Filename = QtWidgets.QLabel(self.gb_Input)
        self.lbl_Filename.setObjectName("lbl_Filename")
        self.gridLayout.addWidget(self.lbl_Filename, 0, 0, 1, 1)
        self.le_Filename = QtWidgets.QLineEdit(self.gb_Input)
        self.le_Filename.setObjectName("le_Filename")
        self.gridLayout.addWidget(self.le_Filename, 0, 1, 1, 1)
        self.FilenamePushButton = QtWidgets.QPushButton(self.gb_Input)
        self.FilenamePushButton.setObjectName("FilenamePushButton")
        self.gridLayout.addWidget(self.FilenamePushButton, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.gb_Input)
        self.Output_groupBox = QtWidgets.QGroupBox(Form)
        self.Output_groupBox.setObjectName("Output_groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Output_groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.Output_groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.Output_groupBox)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 0, 1, 1, 4)
        self.label_2 = QtWidgets.QLabel(self.Output_groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.Output_groupBox)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_2.addWidget(self.lineEdit_3, 1, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.Output_groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 1, 3, 1, 1)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.Output_groupBox)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout_2.addWidget(self.lineEdit_6, 1, 4, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.Output_groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.Output_groupBox)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_2.addWidget(self.lineEdit_4, 2, 2, 1, 3)
        self.label_3 = QtWidgets.QLabel(self.Output_groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 2)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.Output_groupBox)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_2.addWidget(self.lineEdit_5, 3, 2, 1, 3)
        self.ExitPushButton = QtWidgets.QPushButton(self.Output_groupBox)
        self.ExitPushButton.setObjectName("ExitPushButton")
        self.gridLayout_2.addWidget(self.ExitPushButton, 4, 2, 1, 2)
        self.verticalLayout.addWidget(self.Output_groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.gb_Input.setTitle(_translate("Form", "Input"))
        self.lbl_Filename.setText(_translate("Form", "Filename"))
        self.FilenamePushButton.setText(_translate("Form", "Read File and Calculate"))
        self.Output_groupBox.setTitle(_translate("Form", "Output"))
        self.label.setText(_translate("Form", "Pump Name"))
        self.label_2.setText(_translate("Form", "Flow Units"))
        self.label_7.setText(_translate("Form", "Head Units"))
        self.label_4.setText(_translate("Form", "Head Coefficients"))
        self.label_3.setText(_translate("Form", "Efficiency Coefficients"))
        self.ExitPushButton.setText(_translate("Form", "Exit"))

