# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui/packagecollection.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PackageCollectionDialog(object):
    def setupUi(self, PackageCollectionDialog):
        PackageCollectionDialog.setObjectName("PackageCollectionDialog")
        PackageCollectionDialog.resize(493, 304)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(PackageCollectionDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(PackageCollectionDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.titleLabel = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")
        self.gridLayout.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.titleText = QtWidgets.QLineEdit(self.frame)
        self.titleText.setObjectName("titleText")
        self.gridLayout.addWidget(self.titleText, 0, 1, 1, 1)
        self.languagesCombo = QtWidgets.QComboBox(self.frame)
        self.languagesCombo.setObjectName("languagesCombo")
        self.gridLayout.addWidget(self.languagesCombo, 0, 2, 1, 1)
        self.descriptionLabel = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.descriptionLabel.sizePolicy().hasHeightForWidth())
        self.descriptionLabel.setSizePolicy(sizePolicy)
        self.descriptionLabel.setObjectName("descriptionLabel")
        self.gridLayout.addWidget(self.descriptionLabel, 1, 0, 1, 1)
        self.descriptionText = QtWidgets.QTextEdit(self.frame)
        self.descriptionText.setObjectName("descriptionText")
        self.gridLayout.addWidget(self.descriptionText, 1, 1, 2, 1)
        self.packagesButton = QtWidgets.QPushButton(self.frame)
        self.packagesButton.setObjectName("packagesButton")
        self.gridLayout.addWidget(self.packagesButton, 1, 2, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(18, 13, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.icon = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.icon.sizePolicy().hasHeightForWidth())
        self.icon.setSizePolicy(sizePolicy)
        self.icon.setMinimumSize(QtCore.QSize(96, 96))
        self.icon.setMaximumSize(QtCore.QSize(96, 96))
        self.icon.setFrameShape(QtWidgets.QFrame.Box)
        self.icon.setFrameShadow(QtWidgets.QFrame.Plain)
        self.icon.setTextFormat(QtCore.Qt.RichText)
        self.icon.setAlignment(QtCore.Qt.AlignCenter)
        self.icon.setObjectName("icon")
        self.horizontalLayout_2.addWidget(self.icon)
        spacerItem1 = QtWidgets.QSpacerItem(18, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self._2 = QtWidgets.QHBoxLayout()
        self._2.setSpacing(5)
        self._2.setObjectName("_2")
        spacerItem2 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self._2.addItem(spacerItem2)
        self.selectIcon = QtWidgets.QToolButton(self.frame)
        self.selectIcon.setWhatsThis("")
        self.selectIcon.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/raw/pics/view-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.selectIcon.setIcon(icon)
        self.selectIcon.setObjectName("selectIcon")
        self._2.addWidget(self.selectIcon)
        self.clearIcon = QtWidgets.QToolButton(self.frame)
        self.clearIcon.setStatusTip("")
        self.clearIcon.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/raw/pics/edit-clear-locationbar-rtl.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearIcon.setIcon(icon1)
        self.clearIcon.setObjectName("clearIcon")
        self._2.addWidget(self.clearIcon)
        spacerItem3 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self._2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self._2)
        self.gridLayout.addLayout(self.verticalLayout, 2, 2, 1, 1)
        self.verticalLayout_2.addWidget(self.frame)
        spacerItem4 = QtWidgets.QSpacerItem(20, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.buttonBox = QtWidgets.QDialogButtonBox(PackageCollectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.titleLabel.setBuddy(self.titleText)

        self.retranslateUi(PackageCollectionDialog)
        QtCore.QMetaObject.connectSlotsByName(PackageCollectionDialog)

    def retranslateUi(self, PackageCollectionDialog):
        _translate = QtCore.QCoreApplication.translate
        PackageCollectionDialog.setWindowTitle(_translate("PackageCollectionDialog", "Dialog"))
        self.titleLabel.setText(_translate("PackageCollectionDialog", "Title:"))
        self.descriptionLabel.setText(_translate("PackageCollectionDialog", "Description:"))
        self.packagesButton.setText(_translate("PackageCollectionDialog", "Packages"))
        self.icon.setText(_translate("PackageCollectionDialog", "No Icon"))
        self.selectIcon.setToolTip(_translate("PackageCollectionDialog", "Select Photo"))
        self.clearIcon.setToolTip(_translate("PackageCollectionDialog", "Clear Photo"))
import raw_rc
