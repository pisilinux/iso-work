#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# System
import os
import tempfile

# Qt
import QTermWidget

from PyQt5.QtWidgets import (QMessageBox, QMainWindow, QFileDialog,
                             QListWidgetItem, QAction)
from PyQt5.QtGui import QFont  # QIcon,
from PyQt5.QtCore import Qt  # pyqtSignal, QFile,


# UI

# eski kullanıcı arayüzü
# from gui.ui.main import Ui_MainWindow

# yeni kullanıcı arayüzü
from gui.ui.mainv2 import Ui_MainWindow


# Dialogs
from gui.languages import LanguagesDialog
from gui.packages import PackagesDialog
from gui.packagecollection import PackageCollectionDialog

# Progress Dialog
from gui.progress import Progress

# Repository tools
from repotools.packages import (Repository, ExIndexBogus, ExPackageCycle,
                                ExPackageMissing, fetch_uri)
from repotools.project import Project, ExProjectMissing, ExProjectBogus

import gettext

_ = lambda x: gettext.ldgettext("pardusman", x)


def get_finished_status(project):
    status = ("make-repo", "make-live", "pack-live", "make-iso")
    if not os.path.exists(os.path.join(project.work_dir, "finished.txt")):
        return -1

    with open(os.path.join(project.work_dir, "finished.txt"), 'r') as _file:
        state = _file.read()
    state = status.index(state)
    return state


class PackageCollectionListItem(QListWidgetItem):
    def __init__(self, parent, collection, language):
        QListWidgetItem.__init__(self, parent)
        self.collection = collection
        self.setText(collection.translations[language][0])


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, args):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.title = "Pisiman"
        # Terminal

        self.terminal = QTermWidget.QTermWidget()
        self.terminal.setHistorySize(-1)
        self.terminal.setScrollBarPosition(2)
        # self.terminal.setColorScheme(0)
        font = QFont("Droid Sans Mono")  # DejaVu Sans Mono")#Oxygen Mono")
        font.setPointSize(10)
        self.terminal.setTerminalFont(font)

        self.terminal.setColorScheme(
            "/usr/share/qtermwidget5/color-schemes/BreezeModified.colorscheme")

        self.terminalLayout.addWidget(self.terminal)
        self.terminal.show()

        # self.collectionFrame.hide()

        # Arguments
        self.args = args

        # Project
        self.project = Project()

        # Package repository
        self.repo = None

        # Package Selection collections
        self.collections = None

        # File menu
        self.actionNew.triggered.connect(self.slotNew)
        self.actionOpen.triggered.connect(self.slotOpen)
        self.actionSave.triggered.connect(self.slotSave)
        self.actionSaveAs.triggered.connect(self.slotSaveAs)
        self.actionExit.triggered.connect(self.close)

        # Project menu
        self.actionUpdateRepo.triggered.connect(self.slotUpdateRepo)
        self.actionLanguages.triggered.connect(self.slotSelectLanguages)
        self.actionPackages.triggered.connect(self.slotSelectPackages)
        self.actionInstallationImagePackages.triggered.connect(
            self.slotSelectInstallImagePackages)
        self.actionMakeImage.triggered.connect(self.slotMakeImage)

        self.actionMake_Repo.triggered.connect(self.slotMakeRepo)
        self.actionCheck_Repo.triggered.connect(self.slotCheckRepo)
        self.actionMake_Live.triggered.connect(self.slotMakeLive)
        self.actionPack_Live.triggered.connect(self.slotPackLive)
        self.actionMake_Iso.triggered.connect(self.slotMakeIso)

        self.actionRemoveMissingPackages.triggered.connect(
            self.slotRemoveMissingPackages)

        # Browse buttons
        self.pushBrowseRepository.clicked.connect(self.slotBrowseRepository)
        self.pushBrowseWorkFolder.clicked.connect(self.slotBrowseWorkFolder)
        self.pushBrowsePluginPackage.clicked.connect(
            self.slotBrowsePluginPackage)
        self.pushBrowseReleaseFiles.clicked.connect(
            self.slotBrowseReleaseFiles)
        self.btn_browse_iso_output_dir.clicked.connect(
            self.slotBrowseIsoOutputDir)

        # Change Package Selection
        self.pushAddCollection.clicked.connect(self.slotAddPackageCollection)
        self.pushModifyCollection.clicked.connect(
            self.slotModifyPackageCollection)
        self.pushRemoveCollection.clicked.connect(
            self.slotRemovePackageCollection)
        self.pushSetDefaultCollection.clicked.connect(
            self.slotSetDefaultCollection)
        self.checkCollection.stateChanged[int].connect(
            self.slotShowPackageCollection)
        self.listPackageCollection.itemClicked[QListWidgetItem].connect(
            self.slotClickedCollection)

        self.menuCommands.hovered[QAction].connect(self.updateCommands)
        # Initialize
        self.initialize()

        self.updateCommands()

    def initialize(self):
        if len(self.args) == 2:
            self.slotOpen(self.args[1])

    def initializeRepo(self):
        if not self.repo:
            if not self.checkProject():
                return
            if not self.updateRepo():
                return

    def slotNew(self):
        """
            "New" menu item fires this function.
        """
        self.project = Project()
        self.loadProject()

    def slotOpen(self, filename=None):
        """
            "Open..." menu item fires this function.
        """
        if not filename:
            filename = QFileDialog.getOpenFileName(
                self, _("Select project file"), "../project-files",
                "Xml Files (*.xml)")
            filename = filename[0]
        if filename:
            self.project = Project()

            try:
                self.project.open(filename)
            except ExProjectMissing:
                QMessageBox.warning(
                    self, self.title, _("Project file is missing."))
                return
            except ExProjectBogus:
                QMessageBox.warning(
                    self, self.title, _("Project file is corrupt."))
                return
            self.loadProject()
            self.updateCommands()

    def slotSave(self):
        """
            "Save" menu item fires this function.
        """
        if self.project.filename:
            self.updateProject()
            self.project.save()
        else:
            self.slotSaveAs()

    def slotSaveAs(self):
        """
            "Save As..." menu item fires this function.
        """
        filename = QFileDialog.getSaveFileName(
            self, _("Save project"), "../project-files", "Xml Files (*.xml)")
        filename = filename[0]
        if filename:
            self.project.filename = unicode(filename)
            self.slotSave()

    def get_path(self, text):
        print(text)
        if text != "":

            if(os.path.splitext(text)[1] != ""):
                _dir = os.path.dirname(text)
            else:
                _dir = text

            if(_dir.startswith("file:///")):
                _dir = _dir[7:]
            elif(_dir.startswith("file:/")):
                _dir = _dir[5:]

            if not os.path.exists(_dir) or _dir == "":
                _dir = "."
        else:
            _dir = "."

        print(_dir)
        return _dir

    def slotBrowseIsoOutputDir(self):
        _dir = self.get_path(self.le_iso_output_dir.text())

        new_dir = QFileDialog.getExistingDirectory(
            self, _("Select Iso Output Dir"), _dir)

        if new_dir:
            self.le_iso_output_dir.setText(new_dir)

    def slotBrowseRepository(self):
        """
            Browse repository button fires this function.
        """

        _dir = self.get_path(self.lineRepository.text())

        filename = QFileDialog.getOpenFileName(
            self, _("Select repository index"), _dir,
            "Pisi Index Files(*-index.xml *-index.xml.xz)")
        filename = filename[0]
        if filename:
            filename = unicode(filename)
            if filename.startswith("/"):
                filename = "file://%s" % filename
            self.lineRepository.setText(filename)

    def slotBrowsePluginPackage(self):
        """
            Browse plugin package button fires this function.
        """
        _dir = self.get_path(self.linePluginPackage.text())

        filename = QFileDialog.getOpenFileName(
            self, _("Select plugin package"), _dir, "Pisi Files(*.pisi)")
        filename = filename[0]
        if filename:
            self.linePluginPackage.setText(filename)

    def slotBrowseReleaseFiles(self):
        """
            Browse release files button fires this function.
        """
        _dir = self.get_path(self.lineReleaseFiles.text())

        directory = QFileDialog.getExistingDirectory(self, "", _dir)
        if directory:
            self.lineReleaseFiles.setText(directory)

    def slotBrowseWorkFolder(self):
        """
            Browse work folder button fires this function.
        """
        _dir = self.get_path(self.lineWorkFolder.text())

        directory = QFileDialog.getExistingDirectory(self, "", _dir)
        if directory:
            self.lineWorkFolder.setText(directory)

    def slotAddPackageCollection(self):
        if not self.repo:
            self.initializeRepo()

        if not self.project.selected_languages:
            QMessageBox.warning(
                self, self.title, _("Installation Languages is not selected."))
            return

        dialog = PackageCollectionDialog(self, self.repo, self.project)
        if dialog.exec_():
            item = PackageCollectionListItem(
                self.listPackageCollection, dialog.collection,
                self.project.default_language)
            self.project.package_collections.append(item.collection)

            if self.listPackageCollection.count() == 1:
                item.collection.default = "True"

        self.updateCollection()

    def slotModifyPackageCollection(self):
        index = self.listPackageCollection.currentRow()
        item = self.listPackageCollection.item(index)
        if not self.repo:
            self.initializeRepo()

        dialog = PackageCollectionDialog(
            self, self.repo, self.project, item.collection)
        if dialog.exec_():
            if not item.collection._id == dialog.collection._id:
                item.setText(
                    dialog.collection.translations[
                        self.project.default_language][0])
            item.collection = dialog.collection

        self.updateCollection()

    def slotRemovePackageCollection(self):
        for item in self.listPackageCollection.selectedItems():
            self.listPackageCollection.takeItem(
                self.listPackageCollection.row(item))

        self.updateCollection()

    def slotClickedCollection(self, item):
        if item.collection.default == "True":
            if not self.pushSetDefaultCollection.isChecked():
                self.pushSetDefaultCollection.setChecked(True)
        else:
            if self.pushSetDefaultCollection.isChecked():
                self.pushSetDefaultCollection.setChecked(False)

    def slotSetDefaultCollection(self):
        if self.listPackageCollection.currentItem() and \
                not self.listPackageCollection.currentItem(
                ).collection.default:
            self.listPackageCollection.currentItem(
            ).collection.default = "True"
            currentIndex = self.listPackageCollection.currentRow()
            for index in xrange(self.listPackageCollection.count()):
                if index == currentIndex:
                    pass
                else:
                    self.listPackageCollection.item(
                        index).collection.default = ""

            self.pushSetDefaultCollection.setChecked(True)

    def slotShowPackageCollection(self, state):
        if state == Qt.Checked:
            # self.collectionFrame.show()
            self.actionPackages.setVisible(False)
        else:
            # self.collectionFrame.hide()
            self.actionPackages.setVisible(True)

    def slotSelectLanguages(self):
        """
            "Languages..." menu item fires this function.
        """
        dialog = LanguagesDialog(self, self.project.selected_languages)
        if dialog.exec_():
            self.project.default_language = dialog.languages[0]
            self.project.selected_languages = dialog.languages

    def slotSelectPackages(self):
        """
            "Packages..." menu item fires this function.
        """
        if not self.repo:
            if not self.checkProject():
                return
            if not self.updateRepo():
                return

        dialog = PackagesDialog(
            self, self.repo, self.project.selected_packages,
            self.project.selected_components)

        if dialog.exec_():
            self.project.selected_packages = dialog.packages
            self.project.selected_components = dialog.components
            self.project.all_packages = dialog.all_packages

    def slotSelectInstallImagePackages(self):
        """
            "Installation Image Packages..." menu item fires this function.
        """
        if not self.repo:
            if not self.checkProject():
                return
            if not self.updateRepo():
                return

        dialog = PackagesDialog(
            self, self.repo, self.project.selected_install_image_packages,
            self.project.selected_install_image_components)

        if dialog.exec_():
            self.project.selected_install_image_packages = dialog.packages
            self.project.selected_install_image_components = dialog.components
            self.project.all_install_image_packages = dialog.all_packages

    def slotUpdateRepo(self):
        """
            Update repository button fires this function.
        """
        if not self.checkProject():
            return
        self.updateProject()
        self.updateRepo()

    def updateCommands(self):
        state = get_finished_status(self.project)
        # print(state)

        # self.actionCheck_Repo.setEnabled(state >= 0)
        self.actionMake_Live.setEnabled(state >= 0)
        self.actionPack_Live.setEnabled(state >= 1)
        self.actionMake_Iso.setEnabled(state >= 2)

    def slotMakeImage(self):
        """
            Make image button fires this function.
        """
        self.tabWidget.setCurrentIndex(2)
        if os.path.exists(os.path.join(self.project.work_dir, "finished.txt")):
            os.remove(os.path.join(self.project.work_dir, "finished.txt"))

        if not self.repo:
            if not self.checkProject():
                return
            if not self.updateRepo():
                return
        temp_project = tempfile.NamedTemporaryFile(delete=False)
        self.project.save(temp_project.name)
        app_path = self.args[0]
        if app_path[0] != "/":
            app_path = os.path.join(os.getcwd(), app_path)

        # Konsole Mode
        # cmd = 'konsole --noclose --workdir "%s" -e "%s" make "%s"' \
        # % (os.getcwd(), app_path, temp_project.name)
        # subprocess.Popen(["xdg-su", "-u", "root", "-c", cmd])

        cmd = '%s make %s' % (app_path, temp_project.name)
        self.terminal.sendText("sudo %s\n" % cmd)
        self.terminal.setFocus()
        self.updateCommands()

    def slotMakeRepo(self):
        """
            Make image button fires this function.
        """
        self.tabWidget.setCurrentIndex(2)
        if not self.repo:
            if not self.checkProject():
                return
            if not self.updateRepo():
                return
        temp_project = tempfile.NamedTemporaryFile(delete=False)
        self.project.save(temp_project.name)
        app_path = self.args[0]
        if app_path[0] != "/":
            app_path = os.path.join(os.getcwd(), app_path)

        # Konsole Mode
        # cmd = 'konsole --noclose --workdir "%s" -e "%s" make "%s"' \
        # % (os.getcwd(), app_path, temp_project.name)
        # subprocess.Popen(["xdg-su", "-u", "root", "-c", cmd])

        cmd = '%s make-repo %s' % (app_path, temp_project.name)
        self.terminal.sendText("sudo %s\n" % cmd)
        self.terminal.setFocus()
        self.updateCommands()

    def slotCheckRepo(self):
        """
            Make image button fires this function.
        """
        self.tabWidget.setCurrentIndex(2)
        if not self.repo:
            if not self.checkProject():
                return
            if not self.updateRepo():
                return
        temp_project = tempfile.NamedTemporaryFile(delete=False)
        self.project.save(temp_project.name)
        app_path = self.args[0]
        if app_path[0] != "/":
            app_path = os.path.join(os.getcwd(), app_path)

        # Konsole Mode
        # cmd = 'konsole --noclose --workdir "%s" -e "%s" make "%s"' \
        # % (os.getcwd(), app_path, temp_project.name)
        # subprocess.Popen(["xdg-su", "-u", "root", "-c", cmd])

        cmd = '%s check-repo %s' % (app_path, temp_project.name)
        self.terminal.sendText("sudo %s\n" % cmd)
        self.terminal.setFocus()
        self.updateCommands()

    def slotMakeLive(self):
        self.tabWidget.setCurrentIndex(2)
        """
            Make image button fires this function.
        """
        if not self.repo:
            if not self.checkProject():
                return
            if not self.updateRepo():
                return
        temp_project = tempfile.NamedTemporaryFile(delete=False)
        self.project.save(temp_project.name)
        app_path = self.args[0]
        if app_path[0] != "/":
            app_path = os.path.join(os.getcwd(), app_path)

        # Konsole Mode
        # cmd = 'konsole --noclose --workdir "%s" -e "%s" make "%s"' \
        # % (os.getcwd(), app_path, temp_project.name)
        # subprocess.Popen(["xdg-su", "-u", "root", "-c", cmd])

        cmd = '%s make-live %s' % (app_path, temp_project.name)
        self.terminal.sendText("sudo %s\n" % cmd)
        self.terminal.setFocus()
        self.updateCommands()

    def slotPackLive(self):
        """
            Make image button fires this function.
        """
        self.tabWidget.setCurrentIndex(2)
        if not self.repo:
            if not self.checkProject():
                return
            if not self.updateRepo():
                return
        temp_project = tempfile.NamedTemporaryFile(delete=False)
        self.project.save(temp_project.name)
        app_path = self.args[0]
        if app_path[0] != "/":
            app_path = os.path.join(os.getcwd(), app_path)

        # Konsole Mode
        # cmd = 'konsole --noclose --workdir "%s" -e "%s" make "%s"' \
        # % (os.getcwd(), app_path, temp_project.name)
        # subprocess.Popen(["xdg-su", "-u", "root", "-c", cmd])

        cmd = '%s pack-live %s' % (app_path, temp_project.name)
        self.terminal.sendText("sudo %s\n" % cmd)
        self.terminal.setFocus()
        self.updateCommands()

    def slotMakeIso(self):
        """
            Make image button fires this function.
        """
        self.tabWidget.setCurrentIndex(2)
        if not self.repo:
            if not self.checkProject():
                return
            if not self.updateRepo():
                return
        temp_project = tempfile.NamedTemporaryFile(delete=False)
        self.project.save(temp_project.name)
        app_path = self.args[0]
        if app_path[0] != "/":
            app_path = os.path.join(os.getcwd(), app_path)

        # Konsole Mode
        # cmd = 'konsole --noclose --workdir "%s" -e "%s" make "%s"' \
        # % (os.getcwd(), app_path, temp_project.name)
        # subprocess.Popen(["xdg-su", "-u", "root", "-c", cmd])

        cmd = '%s make-iso %s' % (app_path, temp_project.name)
        self.terminal.sendText("sudo %s\n" % cmd)
        self.terminal.setFocus()
        self.updateCommands()

    def updateCollection(self):
        self.project.package_collections = []
        for index in xrange(self.listPackageCollection.count()):
            self.project.package_collections.append(
                self.listPackageCollection.item(index).collection)

    def checkProject(self):
        """
            Checks required fields for the project.
        """
        if not len(self.lineTitle.text()):
            QMessageBox.warning(
                self, self.windowTitle(),  _("Image title is missing."))
            return False
        if not len(self.lineRepository.text()):
            QMessageBox.warning(
                self, self.windowTitle(), _("Repository URL is missing."))
            return False
        if not len(self.lineWorkFolder.text()):
            QMessageBox.warning(
                self, self.windowTitle(),  _("Work folder is missing."))
            return False
        return True

    def updateProject(self):
        """
            Updates project information.
        """
        self.project.title = unicode(self.lineTitle.text())
        self.project.repo_uri = unicode(self.lineRepository.text())
        self.project.work_dir = unicode(self.lineWorkFolder.text())
        self.project.live_repo_uri = unicode(self.lineLiveIsoRepo.text())
        self.project.release_files = unicode(self.lineReleaseFiles.text())
        self.project.plugin_package = unicode(self.linePluginPackage.text())
        self.project.extra_params = unicode(self.lineParameters.text())
        self.project.type = ["install", "live"][self.comboType.currentIndex()]
        self.project.squashfs_comp_type = [
            "xz", "gzip", "lzma", "lzo", "zstd"][self.comboCompression.currentIndex()]

        self.project.iso_output_dir = unicode(self.le_iso_output_dir.text())
        self.project.use_project_dir_as_output_dir = self.check_use_project_dir.isChecked()

        if self.checkCollection.isChecked():
            self.updateCollection()
        else:
            self.listPackageCollection.clear()

    def loadProject(self):
        """
            Loads project information.
        """
        self.lineTitle.setText(unicode(self.project.title))
        self.lineRepository.setText(unicode(self.project.repo_uri))
        self.lineWorkFolder.setText(unicode(self.project.work_dir))
        self.lineLiveIsoRepo.setText(unicode(self.project.live_repo_uri))
        self.lineReleaseFiles.setText(unicode(self.project.release_files))
        self.linePluginPackage.setText(unicode(self.project.plugin_package))
        self.lineParameters.setText(unicode(self.project.extra_params))
        self.comboType.setCurrentIndex(
            ["install", "live"].index(self.project.type))
        self.comboCompression.setCurrentIndex(
            ["xz", "gzip", "lzma", "lzo", "zstd"].index(
                self.project.squashfs_comp_type))

        self.check_use_project_dir.setChecked(self.project.use_project_dir_as_output_dir)
        self.le_iso_output_dir.setText(unicode(self.project.iso_output_dir))

        self.listPackageCollection.clear()
        if self.project.package_collections:
            for index, collection in enumerate(
                    self.project.package_collections):
                PackageCollectionListItem(
                    self.listPackageCollection, collection,
                    self.project.default_language)
                if collection.default:
                    self.listPackageCollection.setCurrentRow(index)
            self.checkCollection.setChecked(True)
        else:
            self.checkCollection.setChecked(False)

    def slotRemoveMissingPackages(self):
        try:
            # curdir = os.getcwd()
            self.tabWidget.setCurrentIndex(2)

            repo = self.project.get_repo()
            repo_path = repo.cache_dir
            if repo_path.startswith("file:///"):
                repo_path = repo_path[7:]
            # print(_("Package index has errors. \
            #     '%s' depends on non-existing '%s'.") % e.args)
            # os.chdir(repo_path)
            if not os.path.exists("{}/../missing.txt".format(repo_path)):
                # os.chdir(curdir)
                QMessageBox.warning(self, self.title, _("Check repo before download.\nIf the repo is checked, there are no lost packages."))
                # print("check repo before download")
                return

            missing_packages = ""
            with open("{}/../missing.txt".format(repo_path)) as file_:
                missing_packages = file_.read()

            missing_packages = missing_packages.split("\n")
            print(missing_packages)
            for pack in missing_packages:
                __package = repo.packages[pack]
                _path = os.path.dirname(os.path.realpath(
                    os.path.join(repo.cache_dir,__package.uri)))
                # print(_path)

                if os.path.exists(_path):
                    __file = os.listdir(_path)
                    print(_path)
                    for f in __file:
                        if os.path.exists(_path + "/" + f):
                            os.remove(_path + "/" + f)

            # os.system("pisi fc {} --runtime-deps".format(
            # os.system("pisi fc {}".format(
            #    " ".join(missing_packages)))
            # os.system("pisi ix --skip-signing")
            QMessageBox.information(self, self.title,
                _("Packages removed that has wrong hash.\nRerun 'Make Inage (Ctrl+R)'."))
            # self.terminal.sendText("pisi fc {} -o {}\n".format(
            #     " ".join(missing_packages), os.path.join(repo_path, _path)))

            # self.terminal.sendText(
            #     "pisi ix --skip-signing {}\n".format(repo_path))

            os.system("rm -f {}/../missing.txt".format(repo_path))
            # os.chdir(curdir)
        except Exception as e:
            print("missing packages could not be downloaded")
            print(e)
            # Progress dialog
            # self.progress = Progress(self)
            # # Update project
            # self.updateProject()
            # # Get repository
            # try:
            #     self.repo = self.project.get_repo(
            #         self.progress, update_repo=True)
            # except ExPackageMissing as e:
            #     self.progress.finished()
            #
            #     curdir = os.getcwd()
            #
            #     repo_path = os.path.dirname(self.project.repo_uri)
            #     if repo_path.startswith("file:///"):
            #         repo_path = repo_path[7:]
            #     print(_("Package index has errors. \
            #         '%s' depends on non-existing '%s'.") % e.args)
            #     os.chdir(repo_path)
            #     os.system("pisi fc {} --runtime-deps".format(
            #         " ".join(e.args[1:])))
            #     os.system("pisi ix --skip-signing")
            #
            #     os.chdir(curdir)
            # else:
            #     self.progress.finished()
            #     break

    def updateRepo(self, update_repo=True):
        """
            Fetches package index and retrieves list of package and components.
        """
        # Progress dialog
        self.progress = Progress(self)
        # Update project
        self.updateProject()
        # Get repository
        try:
            self.repo = self.project.get_repo(
                self.progress, update_repo=update_repo)
        except ExIndexBogus as e:
            # print(e.args[0])
            self.progress.finished()
            QMessageBox.warning(self, self.title, _("Unable to load package \
                index. URL is wrong, or file is corrupt."))
            return False
        except ExPackageCycle as e:
            self.progress.finished()
            cycle = " > ".join(e.args[0])
            QMessageBox.warning(self, self.title, _("Package index has errors.\
                 Cyclic dependency found:\n  %s.") % cycle)
            return False
        except ExPackageMissing as e:
            self.progress.finished()
            QMessageBox.warning(self, self.title, _("Package index has errors.\
            '%s' depends on non-existing '%s'.") % e.args)
            return False
        else:
            self.progress.finished()

        missing_components, missing_packages = self.project.get_missing()
        if len(missing_components):
            QMessageBox.warning(self, self.title, _("There are missing \
            components: {}. Removing.".format(", ".join(missing_components))))
            for component in missing_components:
                if component in self.project.selected_components:
                    self.project.selected_components.remove(component)
                    self.project.selected_install_image_components.remove(
                        component)
            return self.updateRepo(update_repo=False)
            # self.updateRepo(update_repo=False)

        if len(missing_packages):
            QMessageBox.warning(self, self.title, _("There are missing \
            packages: {}. Removing.".format(", ".join(missing_packages))))
            for package in missing_packages:
                if package in self.project.selected_packages:
                    self.project.selected_packages.remove(package)
                    self.project.selected_install_image_packages.remove(
                        package)
            return self.updateRepo(update_repo=False)

        self.progress.finished()

        return True
