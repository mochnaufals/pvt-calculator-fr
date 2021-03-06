# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_about.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutUsDialog(object):
    def setupUi(self, AboutUsDialog):
        AboutUsDialog.setObjectName("AboutUsDialog")
        AboutUsDialog.resize(465, 324)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        AboutUsDialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/oil-barrel.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AboutUsDialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(AboutUsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AboutUsDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.line = QtWidgets.QFrame(AboutUsDialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(AboutUsDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_6 = QtWidgets.QLabel(AboutUsDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setItalic(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.label_9 = QtWidgets.QLabel(AboutUsDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setItalic(True)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.label_9)
        self.label_8 = QtWidgets.QLabel(AboutUsDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setItalic(True)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_2.addWidget(self.label_8)
        self.label_7 = QtWidgets.QLabel(AboutUsDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setItalic(True)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_2.addWidget(self.label_7)
        self.label_5 = QtWidgets.QLabel(AboutUsDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setItalic(True)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.label_4 = QtWidgets.QLabel(AboutUsDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setItalic(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_2 = QtWidgets.QLabel(AboutUsDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_2 = QtWidgets.QFrame(AboutUsDialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_10 = QtWidgets.QLabel(AboutUsDialog)
        self.label_10.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(10)
        font.setItalic(False)
        self.label_10.setFont(font)
        self.label_10.setWordWrap(True)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_3.addWidget(self.label_10)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.line_3 = QtWidgets.QFrame(AboutUsDialog)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.label_11 = QtWidgets.QLabel(AboutUsDialog)
        self.label_11.setEnabled(False)
        self.label_11.setObjectName("label_11")
        self.verticalLayout.addWidget(self.label_11)
        self.label_12 = QtWidgets.QLabel(AboutUsDialog)
        self.label_12.setEnabled(False)
        self.label_12.setObjectName("label_12")
        self.verticalLayout.addWidget(self.label_12)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(2, 10)

        self.retranslateUi(AboutUsDialog)
        QtCore.QMetaObject.connectSlotsByName(AboutUsDialog)

    def retranslateUi(self, AboutUsDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutUsDialog.setWindowTitle(_translate("AboutUsDialog", "Dialog"))
        self.label.setText(_translate("AboutUsDialog", "About Us"))
        self.label_3.setText(_translate("AboutUsDialog", "Developed by the students of Petroleum Engineering, Universitas Pertamina:"))
        self.label_6.setText(_translate("AboutUsDialog", "Ferdiansyah Rahman"))
        self.label_9.setText(_translate("AboutUsDialog", "Mochammad Naufal Septifiandi"))
        self.label_8.setText(_translate("AboutUsDialog", "Humam"))
        self.label_7.setText(_translate("AboutUsDialog", "Elmar Aronov"))
        self.label_5.setText(_translate("AboutUsDialog", "Ilham Budi Nugroho"))
        self.label_4.setText(_translate("AboutUsDialog", "Muhammad Thoriq Atala Ramadhan"))
        self.label_2.setText(_translate("AboutUsDialog", "Muhammad Fahri Amir"))
        self.label_10.setText(_translate("AboutUsDialog", "This program is originally developed to fulfill the final assignment of \'Fluida Reservoir\' course."))
        self.label_11.setText(_translate("AboutUsDialog", "Resources:"))
        self.label_12.setText(_translate("AboutUsDialog", "Icon made by www.flaticon.com"))
import resgui_rc
