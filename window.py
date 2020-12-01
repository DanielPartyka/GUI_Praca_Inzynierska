from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow

rect_list = []

class Ui_AnotherWindow(object):
    def setupUi(self, MainWindow1):
        MainWindow1.setObjectName("AnotherWindow")
        MainWindow1.setEnabled(True)
        MainWindow1.resize(900, 900)
        MainWindow1.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow1)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 889, 874))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.viewport().installEventFilter(self)
        MainWindow1.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow1)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 21))
        self.menubar.setObjectName("menubar")
        MainWindow1.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow1)
        self.statusbar.setObjectName("statusbar")
        MainWindow1.setStatusBar(self.statusbar)
        self.scene_1 = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene_1)
        self.graphicsView.setScene(self.scene_1)
        self.scene_1.clear()
        self.scene_1.addPixmap(QPixmap('Image.png'))
        self.view.fitInView(self.scene_1.sceneRect(), Qt.KeepAspectRatio)

    def setImage(self, image,block_id):
        self.scene_1.clear()
        self.scene_1.addPixmap(QPixmap(image))
        if block_id not in rect_list:
            rect_list.append(block_id)

class MainWindow1(QMainWindow, Ui_AnotherWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow1()
    sys.exit(app.exec_())

