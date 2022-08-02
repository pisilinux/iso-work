# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui/main.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(619, 702)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/raw/pics/pardusman.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineTitle = QtWidgets.QLineEdit(self.frame)
        self.lineTitle.setObjectName("lineTitle")
        self.gridLayout.addWidget(self.lineTitle, 0, 2, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.lineParameters = QtWidgets.QLineEdit(self.frame)
        self.lineParameters.setObjectName("lineParameters")
        self.gridLayout.addWidget(self.lineParameters, 1, 2, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineRepository = QtWidgets.QLineEdit(self.frame)
        self.lineRepository.setObjectName("lineRepository")
        self.gridLayout.addWidget(self.lineRepository, 2, 2, 1, 1)
        self.pushBrowseRepository = QtWidgets.QPushButton(self.frame)
        self.pushBrowseRepository.setObjectName("pushBrowseRepository")
        self.gridLayout.addWidget(self.pushBrowseRepository, 2, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.lineReleaseFiles = QtWidgets.QLineEdit(self.frame)
        self.lineReleaseFiles.setObjectName("lineReleaseFiles")
        self.gridLayout.addWidget(self.lineReleaseFiles, 3, 2, 1, 1)
        self.pushBrowseReleaseFiles = QtWidgets.QPushButton(self.frame)
        self.pushBrowseReleaseFiles.setObjectName("pushBrowseReleaseFiles")
        self.gridLayout.addWidget(self.pushBrowseReleaseFiles, 3, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.linePluginPackage = QtWidgets.QLineEdit(self.frame)
        self.linePluginPackage.setObjectName("linePluginPackage")
        self.gridLayout.addWidget(self.linePluginPackage, 4, 2, 1, 1)
        self.pushBrowsePluginPackage = QtWidgets.QPushButton(self.frame)
        self.pushBrowsePluginPackage.setObjectName("pushBrowsePluginPackage")
        self.gridLayout.addWidget(self.pushBrowsePluginPackage, 4, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)
        self.lineWorkFolder = QtWidgets.QLineEdit(self.frame)
        self.lineWorkFolder.setObjectName("lineWorkFolder")
        self.gridLayout.addWidget(self.lineWorkFolder, 5, 2, 1, 1)
        self.pushBrowseWorkFolder = QtWidgets.QPushButton(self.frame)
        self.pushBrowseWorkFolder.setObjectName("pushBrowseWorkFolder")
        self.gridLayout.addWidget(self.pushBrowseWorkFolder, 5, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.comboType = QtWidgets.QComboBox(self.frame)
        self.comboType.setObjectName("comboType")
        self.comboType.addItem("")
        self.comboType.addItem("")
        self.gridLayout.addWidget(self.comboType, 6, 2, 1, 1)
        self.comboCompression = QtWidgets.QComboBox(self.frame)
        self.comboCompression.setObjectName("comboCompression")
        self.comboCompression.addItem("")
        self.comboCompression.addItem("")
        self.comboCompression.addItem("")
        self.comboCompression.addItem("")
        self.gridLayout.addWidget(self.comboCompression, 6, 3, 1, 1)
        self.checkCollection = QtWidgets.QCheckBox(self.frame)
        self.checkCollection.setObjectName("checkCollection")
        self.gridLayout.addWidget(self.checkCollection, 7, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.frame, 0, 0, 1, 1)
        self.collectionFrame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.collectionFrame.sizePolicy().hasHeightForWidth())
        self.collectionFrame.setSizePolicy(sizePolicy)
        self.collectionFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.collectionFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.collectionFrame.setObjectName("collectionFrame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.collectionFrame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.listPackageCollection = QtWidgets.QListWidget(self.collectionFrame)
        self.listPackageCollection.setObjectName("listPackageCollection")
        self.gridLayout_3.addWidget(self.listPackageCollection, 1, 0, 4, 1)
        self.pushModifyCollection = QtWidgets.QPushButton(self.collectionFrame)
        self.pushModifyCollection.setObjectName("pushModifyCollection")
        self.gridLayout_3.addWidget(self.pushModifyCollection, 2, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.collectionFrame)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)
        self.pushSetDefaultCollection = QtWidgets.QPushButton(self.collectionFrame)
        self.pushSetDefaultCollection.setEnabled(True)
        self.pushSetDefaultCollection.setCheckable(True)
        self.pushSetDefaultCollection.setChecked(True)
        self.pushSetDefaultCollection.setObjectName("pushSetDefaultCollection")
        self.gridLayout_3.addWidget(self.pushSetDefaultCollection, 4, 1, 1, 1)
        self.pushAddCollection = QtWidgets.QPushButton(self.collectionFrame)
        self.pushAddCollection.setObjectName("pushAddCollection")
        self.gridLayout_3.addWidget(self.pushAddCollection, 1, 1, 1, 1)
        self.pushRemoveCollection = QtWidgets.QPushButton(self.collectionFrame)
        self.pushRemoveCollection.setObjectName("pushRemoveCollection")
        self.gridLayout_3.addWidget(self.pushRemoveCollection, 3, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.collectionFrame, 1, 0, 1, 1)
        self.terminalLayout = QtWidgets.QVBoxLayout()
        self.terminalLayout.setObjectName("terminalLayout")
        self.gridLayout_5.addLayout(self.terminalLayout, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 619, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuProject = QtWidgets.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")
        self.menuCommands = QtWidgets.QMenu(self.menuProject)
        self.menuCommands.setObjectName("menuCommands")
        MainWindow.setMenuBar(self.menubar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/raw/pics/document-new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon1)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/raw/pics/document-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon2)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/raw/pics/document-save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon3)
        self.actionSave.setObjectName("actionSave")
        self.actionSaveAs = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/raw/pics/document-save-as.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSaveAs.setIcon(icon4)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/raw/pics/application-exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon5)
        self.actionExit.setObjectName("actionExit")
        self.actionUpdateRepo = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/raw/pics/view-refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUpdateRepo.setIcon(icon6)
        self.actionUpdateRepo.setObjectName("actionUpdateRepo")
        self.actionPackages = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/raw/pics/applications-other.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPackages.setIcon(icon7)
        self.actionPackages.setObjectName("actionPackages")
        self.actionInstallationImagePackages = QtWidgets.QAction(MainWindow)
        self.actionInstallationImagePackages.setIcon(icon7)
        self.actionInstallationImagePackages.setObjectName("actionInstallationImagePackages")
        self.actionLanguages = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/raw/pics/applications-education-language.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLanguages.setIcon(icon8)
        self.actionLanguages.setObjectName("actionLanguages")
        self.actionMakeImage = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/raw/pics/media-optical.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMakeImage.setIcon(icon9)
        self.actionMakeImage.setObjectName("actionMakeImage")
        self.actionMake_Repo = QtWidgets.QAction(MainWindow)
        self.actionMake_Repo.setObjectName("actionMake_Repo")
        self.actionCheck_Repo = QtWidgets.QAction(MainWindow)
        self.actionCheck_Repo.setObjectName("actionCheck_Repo")
        self.actionMake_Live = QtWidgets.QAction(MainWindow)
        self.actionMake_Live.setObjectName("actionMake_Live")
        self.actionPack_Live = QtWidgets.QAction(MainWindow)
        self.actionPack_Live.setObjectName("actionPack_Live")
        self.actionMake_Iso = QtWidgets.QAction(MainWindow)
        self.actionMake_Iso.setObjectName("actionMake_Iso")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuCommands.addAction(self.actionMake_Repo)
        self.menuCommands.addAction(self.actionCheck_Repo)
        self.menuCommands.addSeparator()
        self.menuCommands.addAction(self.actionMake_Live)
        self.menuCommands.addAction(self.actionPack_Live)
        self.menuCommands.addSeparator()
        self.menuCommands.addAction(self.actionMake_Iso)
        self.menuProject.addAction(self.actionUpdateRepo)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionPackages)
        self.menuProject.addAction(self.actionInstallationImagePackages)
        self.menuProject.addAction(self.actionLanguages)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionMakeImage)
        self.menuProject.addAction(self.menuCommands.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuProject.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.lineTitle, self.lineParameters)
        MainWindow.setTabOrder(self.lineParameters, self.lineRepository)
        MainWindow.setTabOrder(self.lineRepository, self.lineReleaseFiles)
        MainWindow.setTabOrder(self.lineReleaseFiles, self.linePluginPackage)
        MainWindow.setTabOrder(self.linePluginPackage, self.lineWorkFolder)
        MainWindow.setTabOrder(self.lineWorkFolder, self.comboType)
        MainWindow.setTabOrder(self.comboType, self.pushBrowseRepository)
        MainWindow.setTabOrder(self.pushBrowseRepository, self.pushBrowseReleaseFiles)
        MainWindow.setTabOrder(self.pushBrowseReleaseFiles, self.pushBrowsePluginPackage)
        MainWindow.setTabOrder(self.pushBrowsePluginPackage, self.pushBrowseWorkFolder)
        MainWindow.setTabOrder(self.pushBrowseWorkFolder, self.comboCompression)
        MainWindow.setTabOrder(self.comboCompression, self.listPackageCollection)
        MainWindow.setTabOrder(self.listPackageCollection, self.pushAddCollection)
        MainWindow.setTabOrder(self.pushAddCollection, self.pushModifyCollection)
        MainWindow.setTabOrder(self.pushModifyCollection, self.pushRemoveCollection)
        MainWindow.setTabOrder(self.pushRemoveCollection, self.pushSetDefaultCollection)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pardusman"))
        self.label.setText(_translate("MainWindow", "Image title"))
        self.lineTitle.setToolTip(_translate("MainWindow", "The title of the Pardus image"))
        self.label_5.setText(_translate("MainWindow", "Extra parameters"))
        self.lineParameters.setToolTip(_translate("MainWindow", "Extra parameters to pass to the kernel command line during boot."))
        self.label_3.setText(_translate("MainWindow", "Repository"))
        self.lineRepository.setToolTip(_translate("MainWindow", "Local or remote URL of the repository index from which the image will be created"))
        self.pushBrowseRepository.setText(_translate("MainWindow", "Browse"))
        self.label_4.setText(_translate("MainWindow", "Release files"))
        self.lineReleaseFiles.setToolTip(_translate("MainWindow", "Path to the local directory which contains metadata about the image like the release notes, etc."))
        self.pushBrowseReleaseFiles.setText(_translate("MainWindow", "Browse"))
        self.label_6.setText(_translate("MainWindow", "Plugin package"))
        self.pushBrowsePluginPackage.setText(_translate("MainWindow", "Browse"))
        self.label_2.setText(_translate("MainWindow", "Work folder"))
        self.lineWorkFolder.setToolTip(_translate("MainWindow", "Path to the directory where Pardusman will work and create the related files and directories"))
        self.pushBrowseWorkFolder.setText(_translate("MainWindow", "Browse"))
        self.label_7.setText(_translate("MainWindow", "Image type"))
        self.comboType.setItemText(0, _translate("MainWindow", "Installation Image"))
        self.comboType.setItemText(1, _translate("MainWindow", "Live Image"))
        self.comboCompression.setItemText(0, _translate("MainWindow", "xz"))
        self.comboCompression.setItemText(1, _translate("MainWindow", "gzip"))
        self.comboCompression.setItemText(2, _translate("MainWindow", "lzma"))
        self.comboCompression.setItemText(3, _translate("MainWindow", "lzo"))
        self.checkCollection.setText(_translate("MainWindow", "Collection Base"))
        self.pushModifyCollection.setText(_translate("MainWindow", "Modify"))
        self.label_9.setText(_translate("MainWindow", "Installation Collection List"))
        self.pushSetDefaultCollection.setText(_translate("MainWindow", "Set as Default"))
        self.pushAddCollection.setText(_translate("MainWindow", "Add"))
        self.pushRemoveCollection.setText(_translate("MainWindow", "Remove"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuProject.setTitle(_translate("MainWindow", "Project"))
        self.menuCommands.setTitle(_translate("MainWindow", "Commands"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionOpen.setText(_translate("MainWindow", "Open..."))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSaveAs.setText(_translate("MainWindow", "Save As..."))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionUpdateRepo.setText(_translate("MainWindow", "Update Repo"))
        self.actionUpdateRepo.setShortcut(_translate("MainWindow", "F5"))
        self.actionPackages.setText(_translate("MainWindow", "Packages..."))
        self.actionInstallationImagePackages.setText(_translate("MainWindow", "Installation Image Packages..."))
        self.actionLanguages.setText(_translate("MainWindow", "Languages..."))
        self.actionMakeImage.setText(_translate("MainWindow", "Make Image"))
        self.actionMake_Repo.setText(_translate("MainWindow", "Make Repo"))
        self.actionCheck_Repo.setText(_translate("MainWindow", "Check Repo"))
        self.actionMake_Live.setText(_translate("MainWindow", "Make Live"))
        self.actionPack_Live.setText(_translate("MainWindow", "Pack Live"))
        self.actionMake_Iso.setText(_translate("MainWindow", "Make Iso"))
import raw_rc
