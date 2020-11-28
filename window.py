# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newwin.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class Ui_AnotherWindow(object):
    def setupUi(self, AnotherWindow):
        AnotherWindow.setObjectName("AnotherWindow")
        AnotherWindow.setEnabled(True)
        AnotherWindow.resize(900, 900)
        self.centralwidget = QtWidgets.QWidget(AnotherWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 889, 874))
        self.graphicsView.setObjectName("graphicsView")
        AnotherWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AnotherWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 21))
        self.menubar.setObjectName("menubar")
        AnotherWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(AnotherWindow)
        self.statusbar.setObjectName("statusbar")
        AnotherWindow.setStatusBar(self.statusbar)

        self.scene_1 = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene_1)
        self.graphicsView.setScene(self.scene_1)
        self.scene_1.clear()
        self.scene_1.addPixmap(QPixmap('Image.png'))
        self.view.fitInView(self.scene_1.sceneRect(), Qt.KeepAspectRatio)

    def setImage(self, image):
        self.scene_1.clear()
        self.scene_1.addPixmap(QPixmap(image))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AnotherWindow = QtWidgets.QMainWindow()
    ui = Ui_AnotherWindow()
    ui.setupUi(AnotherWindow)
    AnotherWindow.show()
    sys.exit(app.exec_())
