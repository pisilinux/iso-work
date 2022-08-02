#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import json
from collections import OrderedDict

# from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QWidget, QFileDialog, QTableWidgetItem

from ui.repowidget import Ui_RepoWidget

# _ = lambda x: QCoreApplication.translate


class RepoWidget(QWidget, Ui_RepoWidget):
    def __init__(self, parent=None, *args):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.pb_repo_open.clicked.connect(self.open)
        
        self.__json_file = ""
        self.__repos = {}
        
        self.pb_repo_up.clicked.connect(self.up)
        
    def open(self):
        # os.getenv("HOME")
        self.__json_file = QFileDialog.getOpenFileName(self, "Open Repo File", ".", "JSON Files (*.json)")[0]
        
        self.load_repos(self.__json_file)
        
    def load_repos(self, json_file):
        try:
            f = open(json_file)
            self.__repos = json.load(f, object_pairs_hook=OrderedDict)
            print(self.__repos)
            f.close()
        except Exception as e:
            print(e)
            return
        
        for name, addr in self.__repos.items():
            self.tw_repo.setRowCount(self.tw_repo.rowCount()+1)
            
            item = QTableWidgetItem(name)
            self.tw_repo.setItem(self.tw_repo.rowCount()-1, 0, item)
            
            item = QTableWidgetItem(addr)
            self.tw_repo.setItem(self.tw_repo.rowCount()-1, 1, item)
            
    def up(self):
        current_row = self.tw_repo.currentRow()
        
        if current_row == 0: return
    
        
        curr_items = (self.tw_repo.item(current_row, 0),
                      self.tw_repo.item(current_row, 1))
        
        prev_items = (self.tw_repo.item(current_row -1, 0),
                      self.tw_repo.item(current_row -1, 1))
        
        self.tw_repo.removeRow(current_row-1)
        self.tw_repo.insertRow(current_row)
        #self.tw_repo.setItem(current_row - 1, 0, curr_items[0])
        #self.tw_repo.setItem(current_row - 1, 1, curr_items[1])
        
        self.tw_repo.setItem(current_row, 0, prev_items[0])
        self.tw_repo.setItem(current_row, 1, prev_items[1])

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)

    w = RepoWidget()
    w.show()

    sys.exit(app.exec_())
