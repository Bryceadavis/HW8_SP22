# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Pump_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(990, 822)
        self.lbl_lnput = QtWidgets.QLabel(Form)
        self.lbl_lnput.setGeometry(QtCore.QRect(30, 10, 55, 16))
        self.lbl_lnput.setObjectName("lbl_lnput")
        self.Input_groupBox = QtWidgets.QGroupBox(Form)
        self.Input_groupBox.setGeometry(QtCore.QRect(30, 40, 931, 101))
        self.Input_groupBox.setTitle("")
        self.Input_groupBox.setObjectName("Input_groupBox")
        self.le_Filename = QtWidgets.QLineEdit(self.Input_groupBox)
        self.le_Filename.setGeometry(QtCore.QRect(82, 21, 791, 41))
        self.le_Filename.setObjectName("le_Filename")
        self.lbl_Filename = QtWidgets.QLabel(self.Input_groupBox)
        self.lbl_Filename.setGeometry(QtCore.QRect(10, 40, 55, 16))
        self.lbl_Filename.setObjectName("lbl_Filename")
        self.FilenamePushButton = QtWidgets.QPushButton(self.Input_groupBox)
        self.FilenamePushButton.setGeometry(QtCore.QRect(80, 70, 211, 28))
        self.FilenamePushButton.setObjectName("FilenamePushButton")
        self.Output_groupBox = QtWidgets.QGroupBox(Form)
        self.Output_groupBox.setGeometry(QtCore.QRect(30, 180, 941, 621))
        self.Output_groupBox.setTitle("")
        self.Output_groupBox.setObjectName("Output_groupBox")
        self.label = QtWidgets.QLabel(self.Output_groupBox)
        self.label.setGeometry(QtCore.QRect(10, 40, 91, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.Output_groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 71, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.Output_groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 141, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.Output_groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 100, 111, 20))
        self.label_4.setObjectName("label_4")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.Output_groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(136, 40, 771, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.Output_groupBox)
        self.lineEdit_3.setGeometry(QtCore.QRect(138, 70, 381, 22))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.Output_groupBox)
        self.lineEdit_4.setGeometry(QtCore.QRect(138, 100, 771, 22))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.Output_groupBox)
        self.lineEdit_5.setGeometry(QtCore.QRect(138, 130, 771, 22))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.ExitPushButton = QtWidgets.QPushButton(self.Output_groupBox)
        self.ExitPushButton.setGeometry(QtCore.QRect(480, 580, 93, 28))
        self.ExitPushButton.setObjectName("ExitPushButton")
        self.label_7 = QtWidgets.QLabel(self.Output_groupBox)
        self.label_7.setGeometry(QtCore.QRect(528, 70, 71, 16))
        self.label_7.setObjectName("label_7")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.Output_groupBox)
        self.lineEdit_6.setGeometry(QtCore.QRect(610, 70, 301, 22))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lbl_Output = QtWidgets.QLabel(Form)
        self.lbl_Output.setGeometry(QtCore.QRect(30, 160, 55, 16))
        self.lbl_Output.setObjectName("lbl_Output")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lbl_lnput.setText(_translate("Form", "Input"))
        self.lbl_Filename.setText(_translate("Form", "Filename"))
        self.FilenamePushButton.setText(_translate("Form", "Read File and Calculate"))
        self.label.setText(_translate("Form", "Pump Name"))
        self.label_2.setText(_translate("Form", "Flow Units"))
        self.label_3.setText(_translate("Form", "Efficiency Coefficients"))
        self.label_4.setText(_translate("Form", "Head Coefficients"))
        self.ExitPushButton.setText(_translate("Form", "Exit"))
        self.label_7.setText(_translate("Form", "Head Units"))
        self.lbl_Output.setText(_translate("Form", "Output"))

