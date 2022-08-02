# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui/rawlanguages.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LanguagesDialog(object):
    def setupUi(self, LanguagesDialog):
        LanguagesDialog.setObjectName("LanguagesDialog")
        LanguagesDialog.resize(467, 350)
        self.gridLayout = QtWidgets.QGridLayout(LanguagesDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(LanguagesDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 2, 1)
        self.label_2 = QtWidgets.QLabel(LanguagesDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.selectedListWidget = QtWidgets.QListWidget(LanguagesDialog)
        self.selectedListWidget.setObjectName("selectedListWidget")
        self.gridLayout.addWidget(self.selectedListWidget, 1, 2, 5, 1)
        self.availableListWidget = QtWidgets.QListWidget(LanguagesDialog)
        self.availableListWidget.setObjectName("availableListWidget")
        self.gridLayout.addWidget(self.availableListWidget, 2, 0, 4, 1)
        spacerItem = QtWidgets.QSpacerItem(49, 153, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(21, 153, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 3, 1, 1)
        self.addButton = QtWidgets.QPushButton(LanguagesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addButton.sizePolicy().hasHeightForWidth())
        self.addButton.setSizePolicy(sizePolicy)
        self.addButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/raw/pics/go-next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addButton.setIcon(icon)
        self.addButton.setObjectName("addButton")
        self.gridLayout.addWidget(self.addButton, 3, 1, 1, 1)
        self.upButton = QtWidgets.QPushButton(LanguagesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.upButton.sizePolicy().hasHeightForWidth())
        self.upButton.setSizePolicy(sizePolicy)
        self.upButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/raw/pics/go-up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.upButton.setIcon(icon1)
        self.upButton.setObjectName("upButton")
        self.gridLayout.addWidget(self.upButton, 3, 3, 1, 1)
        self.removeButton = QtWidgets.QPushButton(LanguagesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeButton.sizePolicy().hasHeightForWidth())
        self.removeButton.setSizePolicy(sizePolicy)
        self.removeButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/raw/pics/go-previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removeButton.setIcon(icon2)
        self.removeButton.setObjectName("removeButton")
        self.gridLayout.addWidget(self.removeButton, 4, 1, 1, 1)
        self.downButton = QtWidgets.QPushButton(LanguagesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downButton.sizePolicy().hasHeightForWidth())
        self.downButton.setSizePolicy(sizePolicy)
        self.downButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/raw/pics/go-down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downButton.setIcon(icon3)
        self.downButton.setObjectName("downButton")
        self.gridLayout.addWidget(self.downButton, 4, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(49, 68, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 5, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(21, 68, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 5, 3, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(LanguagesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 6, 2, 1, 1)

        self.retranslateUi(LanguagesDialog)
        QtCore.QMetaObject.connectSlotsByName(LanguagesDialog)
        LanguagesDialog.setTabOrder(self.addButton, self.removeButton)
        LanguagesDialog.setTabOrder(self.removeButton, self.upButton)
        LanguagesDialog.setTabOrder(self.upButton, self.downButton)
        LanguagesDialog.setTabOrder(self.downButton, self.buttonBox)

    def retranslateUi(self, LanguagesDialog):
        _translate = QtCore.QCoreApplication.translate
        LanguagesDialog.setWindowTitle(_translate("LanguagesDialog", "Languages"))
        self.label.setText(_translate("LanguagesDialog", "Available:"))
        self.label_2.setText(_translate("LanguagesDialog", "Selected:"))
import raw_rc